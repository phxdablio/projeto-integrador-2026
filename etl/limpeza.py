import re
import unicodedata
import pandas as pd

MAPA_BAIRROS = {
    "aguas claras": "Águas Claras",
    "sul aguas claras": "Sul (Águas Claras)",
    "norte aguas claras": "Norte (Águas Claras)",
    "sul (aguas claras)": "Sul (Águas Claras)",
    "norte (aguas claras)": "Norte (Águas Claras)",
}

def _sem_acentos(valor: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", valor) if not unicodedata.combining(c))

def normalizar_bairro(valor: str) -> str:
    original = str(valor or "").strip()
    chave = re.sub(r"\s+", " ", _sem_acentos(original).lower())
    return MAPA_BAIRROS.get(chave, original.title() if original else "")

def somente_digitos(valor: str) -> str:
    return re.sub(r"\D", "", str(valor or ""))

def normalizar_data(valor: str) -> str:
    formatos = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y-%m-%d %H:%M:%S",
    ]

    for formato in formatos:
        try:
            return pd.to_datetime(
                valor, format=formato
            ).strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            continue

    return ""


def limpar_dados(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Padroniza campos e devolve (dados_limpos, auditoria de alterações)."""
    resultado = df.copy().fillna("")
    auditoria = []
    campos = ["cnpj", "telefone", "cep", "bairro_informado", "data_cadastro"]
    for idx, linha in df.iterrows():
        for campo in campos:
            original = str(linha.get(campo, "") or "").strip()
            tratado = original
            criterio = ""
            if campo in ("cnpj", "telefone", "cep"):
                tratado = somente_digitos(original)
                criterio = "Remoção de caracteres não numéricos"
                if campo == "cep" and tratado and len(tratado) != 8:
                    criterio += "; CEP com quantidade de dígitos diferente de 8 sinalizado"
                if campo == "cnpj" and tratado and len(tratado) != 14:
                    criterio += "; CNPJ com quantidade de dígitos diferente de 14 sinalizado"
            elif campo == "bairro_informado":
                tratado = normalizar_bairro(original)
                criterio = "Padronização por mapa explícito de variações conhecidas"
            elif campo == "data_cadastro":
                tratado = normalizar_data(original)
                criterio = "Conversão para YYYY-MM-DD; valor inválido fica vazio"
            resultado.at[idx, campo] = tratado
            if original != tratado:
                auditoria.append({"linha_origem": int(idx) + 2, "id_cliente": linha.get("id_cliente", ""), "campo": campo, "valor_original": original, "valor_tratado": tratado, "criterio": criterio})
    return resultado, pd.DataFrame(auditoria, columns=["linha_origem", "id_cliente", "campo", "valor_original", "valor_tratado", "criterio"])
