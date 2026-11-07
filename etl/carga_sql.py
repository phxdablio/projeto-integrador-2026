
from pathlib import Path
import sqlite3
import pandas as pd


def carregar_sql(
    df: pd.DataFrame,
    caminho_banco: str | Path,
    tabela: str = "clientes"
) -> dict:
    """
    Insere novos clientes e atualiza os existentes
    utilizando id_cliente como identificador.

    Não exclui registros que já existem no banco.
    """

    caminho_banco = Path(caminho_banco)
    caminho_banco.parent.mkdir(parents=True, exist_ok=True)

    if "id_cliente" not in df.columns:
        raise ValueError(
            "A coluna id_cliente não foi encontrada."
        )

    if df["id_cliente"].astype(str).duplicated().any():
        raise ValueError(
            "Existem id_cliente duplicados no arquivo."
        )

    dados = df.copy()
    dados["id_cliente"] = dados["id_cliente"].astype(str)

    colunas = list(dados.columns)

    with sqlite3.connect(caminho_banco) as conexao:

        # Cria a tabela caso ela ainda não exista
        dados.head(0).to_sql(
            tabela,
            conexao,
            if_exists="append",
            index=False
        )

        cursor = conexao.cursor()

        # Verifica as colunas existentes na tabela
        cursor.execute(f'PRAGMA table_info("{tabela}")')
        colunas_banco = {
            linha[1] for linha in cursor.fetchall()
        }

        # Adiciona colunas novas sem apagar os dados antigos
        for coluna in colunas:
            if coluna not in colunas_banco:
                cursor.execute(
                    f'ALTER TABLE "{tabela}" '
                    f'ADD COLUMN "{coluna}"'
                )

        # Atualiza ou insere cada cliente
        inseridos = 0
        atualizados = 0

        placeholders = ", ".join(["?"] * len(colunas))
        nomes_colunas = ", ".join(
            f'"{coluna}"' for coluna in colunas
        )

        comando_insert = (
            f'INSERT INTO "{tabela}" '
            f'({nomes_colunas}) VALUES ({placeholders})'
        )

        colunas_update = [
            coluna for coluna in colunas
            if coluna != "id_cliente"
        ]

        comando_update = (
            f'UPDATE "{tabela}" SET '
            + ", ".join(
                f'"{coluna}" = ?'
                for coluna in colunas_update
            )
            + ' WHERE "id_cliente" = ?'
        )

        for _, registro in dados.iterrows():

            valores = tuple(
                None if pd.isna(registro[coluna])
                else registro[coluna]
                for coluna in colunas
            )

            cursor.execute(
                f'SELECT 1 FROM "{tabela}" '
                'WHERE id_cliente = ?',
                (registro["id_cliente"],)
            )

            existe = cursor.fetchone()

            if existe:
                valores_update = tuple(
                    None if pd.isna(registro[coluna])
                    else registro[coluna]
                    for coluna in colunas_update
                )

                cursor.execute(
                    comando_update,
                    valores_update + (registro["id_cliente"],)
                )

                atualizados += 1

            else:
                cursor.execute(
                    comando_insert,
                    valores
                )

                inseridos += 1

        conexao.commit()

    print("\nCarga SQL concluída!")
    print(f"Novos clientes: {inseridos}")
    print(f"Clientes atualizados: {atualizados}")
    print("Nenhum cliente antigo foi excluído.")

    return {
        "inseridos": inseridos,
        "atualizados": atualizados
    }
