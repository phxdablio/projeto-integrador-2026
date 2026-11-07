import pandas as pd

def enriquecer_dados(df: pd.DataFrame) -> pd.DataFrame:
    """Cria indicadores locais de qualidade; não consulta serviços externos."""
    resultado = df.copy()
    resultado["cnpj_valido_formato"] = resultado["cnpj"].astype(str).str.len().eq(14)
    resultado["cep_valido_formato"] = resultado["cep"].astype(str).str.len().eq(8)
    resultado["telefone_valido_formato"] = resultado["telefone"].astype(str).str.len().isin([10, 11])
    resultado["email_preenchido"] = resultado["email"].astype(str).str.contains(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", regex=True, na=False)
    resultado["bairro_normalizado"] = resultado["bairro_informado"]
    return resultado
