
import argparse
import csv
import os
import sys
from datetime import datetime
from pathlib import Path

# Localiza a pasta principal do projeto
RAIZ_PROJETO = Path(__file__).resolve().parents[2]

# Localiza o projeto Django
PASTA_API = RAIZ_PROJETO / "api"

if str(PASTA_API) not in sys.path:
    sys.path.insert(0, str(PASTA_API))

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

import django

django.setup()

from django.apps import apps
from django.db import transaction


CAMINHO_CSV = (
    RAIZ_PROJETO
    / "data"
    / "processed"
    / "clientes_enriquecidos.csv"
)


def obter_valor(registro, *nomes):
    """Retorna o primeiro campo preenchido encontrado."""
    for nome in nomes:
        valor = registro.get(nome, "")
        if valor is not None and str(valor).strip():
            return str(valor).strip()

    return ""


def converter_data(valor):
    """Converte a data do CSV para o formato aceito pelo Django."""
    formatos = (
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%Y-%m-%d %H:%M:%S",
    )

    for formato in formatos:
        try:
            return datetime.strptime(valor, formato).date()
        except ValueError:
            continue

    raise ValueError(f"Data inválida: {valor}")


def preparar_cliente(registro):
    """Organiza os dados do CSV conforme os campos do modelo Cliente."""

    dados = {
        "id_cliente": obter_valor(registro, "id_cliente"),
        "razao_social": obter_valor(registro, "razao_social"),
        "cnpj_normalizado": obter_valor(
            registro, "cnpj_normalizado", "cnpj"
        ),
        "telefone_normalizado": obter_valor(
            registro, "telefone_normalizado", "telefone"
        ),
        "email": obter_valor(registro, "email"),
        "bairro_normalizado": obter_valor(
            registro, "bairro_normalizado", "bairro_informado"
        ),
        "cep_normalizado": obter_valor(
            registro, "cep_normalizado", "cep"
        ),
    }

    data = obter_valor(
        registro,
        "data_cadastro_normalizado",
        "data_cadastro",
    )

    dados["data_cadastro_normalizado"] = converter_data(data)

    campos_obrigatorios = [
        "id_cliente",
        "razao_social",
        "cnpj_normalizado",
        "telefone_normalizado",
        "email",
        "bairro_normalizado",
        "cep_normalizado",
    ]

    faltantes = [
        campo for campo in campos_obrigatorios
        if not dados[campo]
    ]

    if faltantes:
        raise ValueError(
            "Campos obrigatórios vazios: " + ", ".join(faltantes)
        )

    if len(dados["cnpj_normalizado"]) != 14:
        raise ValueError("CNPJ deve possuir 14 dígitos.")

    if len(dados["cep_normalizado"]) != 8:
        raise ValueError("CEP deve possuir 8 dígitos.")

    if len(dados["telefone_normalizado"]) > 20:
        raise ValueError("Telefone ultrapassa 20 caracteres.")

    return dados


def integrar_clientes(caminho_csv, gravar=False):
    """Lê o CSV e prepara a integração com o banco Django."""

    Cliente = apps.get_model("distribuidora", "Cliente")
    Vendedor = apps.get_model("distribuidora", "Vendedor")

    caminho_csv = Path(caminho_csv)

    if not caminho_csv.exists():
        raise FileNotFoundError(
            f"Arquivo CSV não encontrado: {caminho_csv}"
        )

    inseridos = 0
    atualizados = 0
    ignorados = 0
    erros = []

    with caminho_csv.open(
        "r", encoding="utf-8-sig", newline=""
    ) as arquivo:

        leitor = csv.DictReader(arquivo, delimiter=";")

        for numero, registro in enumerate(leitor, start=2):
            try:
                dados = preparar_cliente(registro)

                nome_vendedor = obter_valor(
                    registro,
                    "vendedor_responsavel",
                    "nome_vendedor",
                    "vendedor",
                )

                if not nome_vendedor:
                    raise ValueError("Vendedor não informado.")

                if not gravar:
                    inseridos += 1
                    continue

                with transaction.atomic():
                    vendedor, _ = Vendedor.objects.get_or_create(
                        nome_vendedor=nome_vendedor
                    )

                    dados["vendedor"] = vendedor

                    _, criado = Cliente.objects.update_or_create(
                        id_cliente=dados["id_cliente"],
                        defaults=dados,
                    )

                if criado:
                    inseridos += 1
                else:
                    atualizados += 1

            except Exception as erro:
                ignorados += 1
                erros.append(
                    f"Linha {numero}: {erro}"
                )

    print("\nResultado da integração")
    print(f"Inseridos: {inseridos}")
    print(f"Atualizados: {atualizados}")
    print(f"Ignorados: {ignorados}")

    for erro in erros:
        print(erro)

    if not gravar:
        print("\nSIMULAÇÃO: nenhum dado foi gravado no banco.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Integra os clientes do ETL com o Django."
    )

    parser.add_argument(
        "--gravar",
        action="store_true",
        help="Autoriza gravar os dados no banco Django."
    )

    parser.add_argument(
        "--arquivo",
        default=str(CAMINHO_CSV),
        help="Caminho do CSV enriquecido."
    )

    argumentos = parser.parse_args()

    integrar_clientes(
        argumentos.arquivo,
        gravar=argumentos.gravar,
    )
