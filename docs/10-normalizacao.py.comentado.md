
# normalizacao.py — Arquivo Comentado

## 1. Importações

```python
import difflib
import re
from datetime import date, datetime
```

- `difflib` → permite identificar nomes de bairros semelhantes aos nomes oficiais cadastrados.
- `re` → disponibiliza expressões regulares para limpar e padronizar textos.
- `date` e `datetime` → permitem reconhecer e converter diferentes representações de datas.

---

## 2. Lista de bairros oficiais

```python
BAIRROS_OFICIAIS = [
    "Plano Piloto", "Gama", "Taguatinga", "Brazlândia",
    "Sobradinho I", "Planaltina", "Paranoá",
    # ... demais localidades
    "Arniqueira", "Arapoanga", "Água Quente",
]
```

- `BAIRROS_OFICIAIS` → armazena os nomes padronizados das localidades utilizadas pelo sistema.
- A lista serve como referência para corrigir variações de escrita durante o cadastro.

---

## 3. Função limpar_texto()

```python
def limpar_texto(valor, padrao=""):
    if valor is None:
        return padrao

    texto = str(valor).strip()

    if texto.lower() in (
        "", "none", "nan", "null",
        "não informado", "nao informado"
    ):
        return padrao

    return texto
```

- `valor is None` → substitui valores nulos pelo padrão informado.
- `str(valor).strip()` → converte o valor em texto e remove espaços nas extremidades.
- `texto.lower()` → permite identificar valores considerados vazios sem diferenciar maiúsculas e minúsculas.
- `padrao` → define o valor utilizado quando a entrada não possui informação válida.

## 4. Função normalizar_cnpj()

```python
def normalizar_cnpj(valor):
    digitos = re.sub(
        r"\D", "", limpar_texto(valor, padrao="")
    )
    return digitos[:14]
```

- `limpar_texto()` → prepara o valor recebido.
- `re.sub(r"\D", "", ...)` → remove pontos, barras, hífens e outros caracteres não numéricos.
- `digitos[:14]` → mantém somente os primeiros 14 dígitos.

## 5. Função normalizar_telefone()

```python
def normalizar_telefone(valor):
    texto = limpar_texto(valor, padrao="")

    if not texto:
        return None

    sem_ddi = re.sub(
        r"^\+?55", "", texto
    )

    digitos = re.sub(r"\D", "", sem_ddi)

    return digitos[:20] if digitos else None
```

- `re.sub()` → remove o prefixo `55` no início, conforme a expressão regular apresentada.
- `r"\D"` → elimina caracteres não numéricos.
- `digitos[:20]` → limita o resultado a 20 dígitos.
- Retorna `None` quando não existem dígitos para armazenar.

## 6. Função normalizar_cep()

```python
def normalizar_cep(valor):
    texto = limpar_texto(valor, padrao="")

    if not texto:
        return None

    base = texto.split(".")[0]
    digitos = re.sub(r"\D", "", base)

    if len(digitos) != 8 or int(digitos) == 0:
        return None

    return digitos
```

- `texto.split(".")[0]` → utiliza apenas a parte anterior ao primeiro ponto.
- `re.sub(r"\D", "", base)` → remove caracteres não numéricos.
- `len(digitos) != 8` → rejeita CEPs com quantidade incorreta de dígitos.
- `int(digitos) == 0` → rejeita valores compostos exclusivamente por zeros.
- Retorna `None` para valores que não atendem às condições.

## 7. Função normalizar_bairro()

```python
def normalizar_bairro(valor):
    texto = limpar_texto(valor, padrao="")

    if not texto:
        return "Não informado"

    sem_uf = re.sub(
        r"\s*[-/]?\s*df\s*$",
        "",
        texto,
        flags=re.IGNORECASE
    ).strip()

    bairros_lower = [
        b.lower() for b in BAIRROS_OFICIAIS
    ]

    matches = difflib.get_close_matches(
        sem_uf.lower(),
        bairros_lower,
        n=1,
        cutoff=0.5
    )

    if matches:
        return BAIRROS_OFICIAIS[
            bairros_lower.index(matches[0])
        ]

    return sem_uf.title()[:100]
```

- `bairros_lower` → cria uma lista auxiliar com nomes em letras minúsculas.
- `difflib.get_close_matches()` → procura o nome oficial mais semelhante ao texto informado.
- `n=1` → retorna no máximo uma correspondência.
- `cutoff=0.5` → estabelece o limite mínimo de similaridade.
- `title()[:100]` → formata e limita o texto quando nenhuma correspondência é encontrada.

## 8. Função normalizar_data()

```python
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

    for fmt in (
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y/%m/%d"
    ):
        try:
            return datetime.strptime(
                texto, fmt
            ).date()
        except ValueError:
            continue

    return None
```

- `isinstance(valor, datetime)` → extrai a data de um objeto que também contém horário.
- `isinstance(valor, date)` → mantém valores que já representam datas.
- `datetime.strptime()` → interpreta a entrada conforme os formatos aceitos.
- `except ValueError` → permite tentar o próximo formato quando uma conversão falha.

## 9. Integração com o models.py

- As funções de normalização são utilizadas no método `save()` do modelo `Cliente`.

- Esse processo contribui para a padronização dos registros, reduzindo diferenças de formatação entre dados cadastrados.
