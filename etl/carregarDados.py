"""
Carrega o CSV tratado (clientes_tratados.csv) para o banco de dados.

Uso (a partir da pasta etl):
    python carregar_banco.py
"""
import sqlite3
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Configuração: ajuste estes valores para o seu projeto
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / ".." / "data" / "clientes_tratados.csv"
DB_PATH = BASE_DIR / ".." / "db.sqlite3"   # caminho do seu banco SQLite
TABELA = "clientes"                        # nome da tabela de destino

# 'append'  -> adiciona as linhas na tabela existente (use com tabelas do Django)
# 'replace' -> apaga e recria a tabela (útil só em desenvolvimento)
IF_EXISTS = "append"


def carregar_csv(caminho: Path) -> pd.DataFrame:
    df = pd.read_csv(caminho, sep=";", encoding="utf-8", dtype=str)

    # Datas no padrão ISO (AAAA-MM-DD); valores inválidos viram NULL no banco
    if "data_cadastro" in df.columns:
        datas = pd.to_datetime(df["data_cadastro"], errors="coerce")
        df["data_cadastro"] = datas.dt.strftime("%Y-%m-%d")

    # NaN -> None, para o SQLite gravar NULL
    return df.astype(object).where(df.notna(), None)


def enviar_para_banco(df: pd.DataFrame, db_path: Path, tabela: str, if_exists: str) -> None:
    with sqlite3.connect(db_path) as conn:
        df.to_sql(tabela, conn, if_exists=if_exists, index=False)
        total = conn.execute(f"SELECT COUNT(*) FROM {tabela}").fetchone()[0]
    print(f"--> {len(df)} linhas enviadas. Total atual na tabela '{tabela}': {total}")


def main() -> None:
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV não encontrado: {CSV_PATH}")

    df = carregar_csv(CSV_PATH)
    print(f"CSV lido: {df.shape[0]} linhas, {df.shape[1]} colunas")
    enviar_para_banco(df, DB_PATH, TABELA, IF_EXISTS)


if __name__ == "__main__":
    main()