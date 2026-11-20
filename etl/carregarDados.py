

import os
import sys
import re
from pathlib import Path

import pandas as pd

# =====================================================
# 1. CONFIGURAÇÃO DO PROJETO DJANGO
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent
API_DIR = BASE_DIR / "api"
CSV_PATH = BASE_DIR / "data" / "clientes_tratados.csv"

sys.path.insert(0, str(API_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from django.db import transaction
from distribuidora.models import Cliente, Vendedor


# =====================================================
# 2. FUNÇÃO DE NORMALIZAÇÃO
# =====================================================

def somente_numeros(valor):
    if pd.isna(valor):
        return ""

    return re.sub(r"\D", "", str(valor))


# =====================================================
# 3. LEITURA DO CSV
# =====================================================

def carregar_csv():

    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"CSV não encontrado: {CSV_PATH}"
        )

    df = pd.read_csv(
        CSV_PATH,
        sep=";",
        encoding="utf-8",
        dtype=str
    )

    df.columns = df.columns.str.strip().str.lower()

    colunas_obrigatorias = [
        "id_cliente",
        "razao_social",
        "cnpj",
        "telefone",
        "email",
        "bairro_informado",
        "cep",
        "data_cadastro",
        "vendedor_responsavel"
    ]

    faltantes = [
        coluna for coluna in colunas_obrigatorias
        if coluna not in df.columns
    ]

    if faltantes:
        raise ValueError(
            f"Colunas ausentes no CSV: {faltantes}"
        )

    print("CSV carregado com sucesso!")
    print("Quantidade de registros:", len(df))
    print("Colunas:", df.columns.tolist())

    return df


# =====================================================
# 4. TRANSFORMAÇÃO DOS DADOS
# =====================================================

def transformar_cliente(linha):

    cnpj = somente_numeros(linha["cnpj"])
    telefone = somente_numeros(linha["telefone"])
    cep = somente_numeros(linha["cep"])

    data = pd.to_datetime(
        linha["data_cadastro"],
        errors="coerce",
        dayfirst=True
    )

    if pd.isna(data):
        raise ValueError(
            f"Data de cadastro inválida: "
            f"{linha['data_cadastro']}"
        )

    cliente = {
        "id_cliente": str(linha["id_cliente"]).strip(),
        "razao_social": str(linha["razao_social"]).strip(),
        "cnpj_normalizado": cnpj,
        "telefone_normalizado": telefone,
        "email": (
            str(linha["email"]).strip()
            if pd.notna(linha["email"])
            else ""
        ),
        "bairro_normalizado": str(
            linha["bairro_informado"]
        ).strip(),
        "cep_normalizado": cep,
        "data_cadastro_normalizado": data.date()
    }

    if not cliente["id_cliente"]:
        raise ValueError("ID do cliente vazio.")

    if not cliente["razao_social"]:
        raise ValueError(
            f"Razão social vazia: {cliente['id_cliente']}"
        )

    if len(cnpj) > 14 or len(telefone) > 20 or len(cep) > 8:
        raise ValueError(
            f"Campo numérico acima do limite: "
            f"{cliente['id_cliente']}"
        )

    return cliente


# =====================================================
# 5. CARGA NO SQLITE ATRAVÉS DO DJANGO ORM
# =====================================================

def carregar_banco(df):

    inseridos = 0
    atualizados = 0

    with transaction.atomic():

        for indice, linha in df.iterrows():

            dados = transformar_cliente(linha)

            nome_vendedor = str(
                linha["vendedor_responsavel"]
            ).strip()

            if pd.isna(linha["vendedor_responsavel"]) or not nome_vendedor:
                raise ValueError(
                    f"Vendedor não informado na linha {indice + 2}"
                )

            vendedor, _ = Vendedor.objects.get_or_create(
                nome_vendedor=nome_vendedor
            )

            dados["vendedor"] = vendedor

            cliente, criado = Cliente.objects.update_or_create(
                id_cliente=dados.pop("id_cliente"),
                defaults=dados
            )

            if criado:
                inseridos += 1
            else:
                atualizados += 1

    print("\n========== RESULTADO DA CARGA ==========")
    print("Clientes inseridos:", inseridos)
    print("Clientes atualizados:", atualizados)
    print("Total de clientes:", Cliente.objects.count())
    print("Total de vendedores:", Vendedor.objects.count())
    print("Banco utilizado:", Cliente.objects.db)
    print("Carga concluída!")


# =====================================================
# 6. EXECUÇÃO PRINCIPAL
# =====================================================

def main():

    print("Iniciando integração ETL com Django...")

    df = carregar_csv()

    carregar_banco(df)


if __name__ == "__main__":
    main()
