import difflib
import re
from datetime import date, datetime

BAIRROS_OFICIAIS = [
    "Plano Piloto", "Gama", "Taguatinga", "Brazlândia", "Sobradinho I",
    "Planaltina", "Paranoá", "Núcleo Bandeirante", "Ceilândia", "Guará I",
    "Guará II", "Cruzeiro", "Samambaia", "Santa Maria", "São Sebastião",
    "Recanto das Emas", "Lago Sul", "Riacho Fundo I", "Lago Norte",
    "Candangolândia", "Águas Claras", "Riacho Fundo II", "Sudoeste/Octogonal",
    "Varjão", "Park Way", "SCIA", "Sobradinho II", "Jardim Botânico",
    "Itapoã", "SIA", "Vicente Pires", "Fercal", "Sol Nascente/Pôr do Sol",
    "Arniqueira", "Arapoanga", "Água Quente",
]


def limpar_texto(valor, padrao=""):
    if valor is None:
        return padrao
    texto = str(valor).strip()
    if texto.lower() in ("", "none", "nan", "null", "não informado", "nao informado"):
        return padrao
    return texto


def normalizar_cnpj(valor):
    digitos = re.sub(r"\D", "", limpar_texto(valor, padrao=""))
    return digitos[:14]


def normalizar_telefone(valor):
    texto = limpar_texto(valor, padrao="")
    if not texto:
        return None
    sem_ddi = re.sub(r"^\+?55", "", texto)
    digitos = re.sub(r"\D", "", sem_ddi)
    return digitos[:20] if digitos else None


def normalizar_cep(valor):
    texto = limpar_texto(valor, padrao="")
    if not texto:
        return None
    base = texto.split(".")[0]
    digitos = re.sub(r"\D", "", base)
    if len(digitos) != 8 or int(digitos) == 0:
        return None
    return digitos


def normalizar_bairro(valor):
    texto = limpar_texto(valor, padrao="")
    if not texto:
        return "Não informado"

    sem_uf = re.sub(r"\s*[-/]?\s*df\s*$", "", texto, flags=re.IGNORECASE).strip()
    bairros_lower = [b.lower() for b in BAIRROS_OFICIAIS]
    matches = difflib.get_close_matches(sem_uf.lower(), bairros_lower, n=1, cutoff=0.5)

    if matches:
        return BAIRROS_OFICIAIS[bairros_lower.index(matches[0])]

    return sem_uf.title()[:100]


def normalizar_data(valor):
    if valor is None:
        return None
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, date):
        return valor

    texto = limpar_texto(valor, padrao="")
    if not texto:
        return None

    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(texto, fmt).date()
        except ValueError:
            continue

    return None
