import re
import unicodedata
from typing import Any

import requests

from .cache_cep import obter_cache, guardar_cache


# Endereço da API ViaCEP
VIACEP_URL = "https://viacep.com.br/ws/{cep}/json/"


# Remove caracteres que não sejam números
def somente_digitos(valor: Any) -> str:
    return re.sub(r"\D", "", str(valor or ""))


# Padroniza textos para comparação
def normalizar_texto(valor: Any) -> str:

    texto = unicodedata.normalize("NFKD", str(valor or ""))

    texto = "".join(
        caractere
        for caractere in texto
        if not unicodedata.combining(caractere)
    )

    return " ".join(texto.casefold().strip().split())


# Compara o bairro informado com o bairro da ViaCEP
def comparar_bairro(bairro_informado: str, bairro_api: str) -> str:

    if not bairro_informado or not bairro_api:
        return "nao_comparavel"

    if normalizar_texto(bairro_informado) == normalizar_texto(bairro_api):
        return "compativel"

    return "divergente"


# Consulta o CEP na API ViaCEP
def consultar_cep(cep: str, timeout: int = 8) -> dict[str, Any]:

    cep_limpo = somente_digitos(cep)

    if len(cep_limpo) != 8:
        return {
            "status": "cep_invalido",
            "cep_consultado": cep_limpo
        }

    # Verifica se o CEP já está armazenado
    cache = obter_cache(cep_limpo)

    if cache is not None:
        return {
            **cache,
            "origem_consulta": "cache"
        }

    try:

        resposta = requests.get(
            VIACEP_URL.format(cep=cep_limpo),
            timeout=timeout
        )

        resposta.raise_for_status()

        dados = resposta.json()

    except (requests.RequestException, ValueError) as erro:

        return {
            "status": "erro_consulta",
            "cep_consultado": cep_limpo,
            "detalhe": str(erro)
        }

    if dados.get("erro"):

        resultado = {
            "status": "cep_nao_encontrado",
            "cep_consultado": cep_limpo
        }

    else:

        resultado = {
            "status": "encontrado",
            "cep_consultado": cep_limpo,
            "cep_api": somente_digitos(dados.get("cep")),
            "logradouro_api": dados.get("logradouro", ""),
            "bairro_api": dados.get("bairro", ""),
            "cidade_api": dados.get("localidade", ""),
            "uf_api": dados.get("uf", "")
        }

    # Guarda o resultado para consultas futuras
    guardar_cache(cep_limpo, resultado)

    return {
        **resultado,
        "origem_consulta": "api"
    }


# Enriquece um registro de cliente e registra as alterações
def enriquecer_registro(
    registro: dict[str, Any],
    auditoria=None
) -> dict[str, Any]:

    resultado = dict(registro)

    # Guarda os valores originais para comparação e auditoria
    bairro_original = str(
        registro.get("bairro_informado") or ""
    ).strip()

    bairro_normalizado_original = str(
        registro.get("bairro_normalizado") or ""
    ).strip()

    cidade_original = str(
        registro.get("cidade") or ""
    ).strip()

    uf_original = str(
        registro.get("uf") or ""
    ).strip()

    cep = (
        registro.get("cep_normalizado")
        or registro.get("cep", "")
    )

    consulta = consultar_cep(str(cep))

    resultado["cep_api_status"] = consulta.get("status", "")
    resultado["bairro_api"] = consulta.get("bairro_api", "")
    resultado["cidade_api"] = consulta.get("cidade_api", "")
    resultado["uf_api"] = consulta.get("uf_api", "")
    resultado["logradouro_api"] = consulta.get("logradouro_api", "")
    resultado["cep_api_origem"] = consulta.get("origem_consulta", "")

    # Compara o bairro original com o retornado pela API
    status_bairro = comparar_bairro(
        bairro_original,
        str(consulta.get("bairro_api", ""))
    )

    resultado["bairro_cep_status"] = status_bairro

    # Só preenche informações quando a consulta foi bem-sucedida
    if consulta.get("status") == "encontrado":

        campos = [
            (
                "bairro_normalizado",
                bairro_normalizado_original,
                consulta.get("bairro_api", ""),
                "Preenchimento de bairro vazio com informação do ViaCEP"
            ),
            (
                "cidade",
                cidade_original,
                consulta.get("cidade_api", ""),
                "Preenchimento de cidade vazia com informação do ViaCEP"
            ),
            (
                "uf",
                uf_original,
                consulta.get("uf_api", ""),
                "Preenchimento de UF vazia com informação do ViaCEP"
            )
        ]

        for campo, original, valor_api, criterio in campos:

            if not original and valor_api:

                resultado[campo] = valor_api

                if auditoria is not None:
                    auditoria.append({
                        "id_cliente": registro.get("id_cliente", ""),
                        "campo": campo,
                        "valor_original": original,
                        "valor_tratado": valor_api,
                        "criterio": criterio,
                        "fonte": consulta.get("origem_consulta", "api"),
                        "cep_consultado": consulta.get("cep_consultado", "")
                    })

        # Registra o bairro divergente sem substituir o informado
        if status_bairro == "divergente" and auditoria is not None:

            auditoria.append({
                "id_cliente": registro.get("id_cliente", ""),
                "campo": "bairro_informado",
                "valor_original": bairro_original,
                "valor_tratado": bairro_original,
                "criterio": "Divergência entre bairro informado e bairro retornado pelo ViaCEP; valor original preservado",
                "fonte": consulta.get("origem_consulta", "api"),
                "cep_consultado": consulta.get("cep_consultado", "")
            })

    return resultado

    