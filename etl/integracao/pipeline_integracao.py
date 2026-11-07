from pathlib import Path
import pandas as pd

from etl.extracao import extrair_dados
from etl.limpeza import limpar_dados
from etl.enriquecimento import enriquecer_dados
from etl.auditoria import salvar_auditoria
from .enriquecimento_cep import enriquecer_registro


RAIZ_PROJETO = Path(__file__).resolve().parents[2]

CAMINHO_ENTRADA = (
    RAIZ_PROJETO / "data" / "raw"
    / "clientes_distribuidora_vetor.csv"
)

CAMINHO_PROCESSADO = (
    RAIZ_PROJETO / "data" / "processed"
    / "clientes_enriquecidos.csv"
)

CAMINHO_AUDITORIA = (
    RAIZ_PROJETO / "reports"
    / "auditoria_integracao_cep.csv"
)


def executar_pipeline():
    """Executa o ETL e acrescenta o enriquecimento de CEP."""

    print("Iniciando pipeline de integração...")

    # 1. Extração
    dados = extrair_dados(CAMINHO_ENTRADA)

    # 2. Limpeza
    dados, auditoria_limpeza = limpar_dados(dados)

    # 3. Enriquecimento original
    dados = enriquecer_dados(dados)

    # 4. Enriquecimento dos CEPs e coleta da auditoria
    auditoria_cep = []

    registros = dados.to_dict(orient="records")

    registros_enriquecidos = [
        enriquecer_registro(registro, auditoria_cep)
        for registro in registros
    ]

    dados = pd.DataFrame(registros_enriquecidos)

    # 5. Salvar dados processados
    CAMINHO_PROCESSADO.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    dados.to_csv(
        CAMINHO_PROCESSADO,
        index=False,
        sep=";",
        encoding="utf-8-sig"
    )

    # 6. Auditoria do enriquecimento de CEP
    colunas_auditoria_cep = [
        "id_cliente",
        "campo",
        "valor_original",
        "valor_tratado",
        "criterio",
        "fonte",
        "cep_consultado"
    ]

    df_auditoria_cep = pd.DataFrame(
        auditoria_cep,
        columns=colunas_auditoria_cep
    )

    salvar_auditoria(
        df_auditoria_cep,
        CAMINHO_AUDITORIA
    )

    # 7. Auditoria das alterações da limpeza
    CAMINHO_AUDITORIA_LIMPEZA = (
        RAIZ_PROJETO / "reports" / "auditoria_limpeza.csv"
    )

    salvar_auditoria(
        auditoria_limpeza,
        CAMINHO_AUDITORIA_LIMPEZA
    )

    print("\nPipeline concluído!")
    print(f"Registros processados: {len(dados)}")
    print(f"Arquivo gerado: {CAMINHO_PROCESSADO}")
    print(f"Auditoria gerada: {CAMINHO_AUDITORIA}")

    return dados


if __name__ == "__main__":
    executar_pipeline()
