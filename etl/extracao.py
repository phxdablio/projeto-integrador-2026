from pathlib import Path
import pandas as pd

COLUNAS_OBRIGATORIAS = ["id_cliente", "razao_social", "cnpj", "telefone", "email", "bairro_informado", "cep", "cidade", "uf", "data_cadastro", "vendedor_responsavel"]

def extrair_dados(caminho: str | Path) -> pd.DataFrame:
    """Lê o CSV original como texto para preservar zeros à esquerda e formatos."""
    caminho = Path(caminho)
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {caminho}")
    df = pd.read_csv(caminho, sep=";", dtype=str, keep_default_na=False, encoding="utf-8-sig")
    faltantes = [col for col in COLUNAS_OBRIGATORIAS if col not in df.columns]
    if faltantes:
        raise ValueError(f"Colunas obrigatórias ausentes: {', '.join(faltantes)}")
    return df
