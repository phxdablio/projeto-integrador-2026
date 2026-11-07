from pathlib import Path
from extracao import extrair_dados
from limpeza import limpar_dados
from enriquecimento import enriquecer_dados
from auditoria import salvar_auditoria
from carga_sql import carregar_sql

RAIZ = Path(__file__).resolve().parents[1]
ARQUIVO_ENTRADA = RAIZ / "data" / "raw" / "clientes_distribuidora_vetor.csv"
ARQUIVO_TRATADO = RAIZ / "data" / "processed" / "clientes_tratados.csv"
ARQUIVO_AUDITORIA = RAIZ / "reports" / "auditoria.csv"
BANCO = RAIZ / "data" / "processed" / "distribuidora_vetor.db"

def executar_pipeline():
    dados = extrair_dados(ARQUIVO_ENTRADA)
    dados_limpos, log = limpar_dados(dados)
    dados_enriquecidos = enriquecer_dados(dados_limpos)
    ARQUIVO_TRATADO.parent.mkdir(parents=True, exist_ok=True)
    dados_enriquecidos.to_csv(ARQUIVO_TRATADO, index=False, sep=";", encoding="utf-8-sig")
    salvar_auditoria(log, ARQUIVO_AUDITORIA)
    carregar_sql(dados_enriquecidos, BANCO)
    print(f"ETL concluído: {len(dados_enriquecidos)} registros processados.")
    print(f"Base tratada: {ARQUIVO_TRATADO}")
    print(f"Auditoria: {ARQUIVO_AUDITORIA}")
    print(f"Banco SQLite: {BANCO}")
    return dados_enriquecidos

if __name__ == "__main__":
    executar_pipeline()
