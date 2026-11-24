import json
from pathlib import Path
from typing import Any

# Local onde o cache será armazenado
CACHE_PATH = Path(__file__).resolve().parents[2] / "data" / "cache" / "ceps.json"


# Carrega os CEPs que já foram consultados
def carregar_cache(caminho: Path = CACHE_PATH) -> dict[str, Any]:

    if not caminho.exists():
        return {}

    try:
        return json.loads(caminho.read_text(encoding="utf-8"))

    except (json.JSONDecodeError, OSError):
        return {}


# Salva os resultados das consultas
def salvar_cache(cache: dict[str, Any], caminho: Path = CACHE_PATH) -> None:

    caminho.parent.mkdir(parents=True, exist_ok=True)

    temporario = caminho.with_suffix(".tmp")

    temporario.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    temporario.replace(caminho)


# Procura um CEP que já foi consultado
def obter_cache(cep: str, caminho: Path = CACHE_PATH):

    cache = carregar_cache(caminho)

    return cache.get(cep)


# Guarda um novo resultado no cache
def guardar_cache(cep: str, dados: dict[str, Any], caminho: Path = CACHE_PATH) -> None:

    cache = carregar_cache(caminho)

    cache[cep] = dados

    salvar_cache(cache, caminho)