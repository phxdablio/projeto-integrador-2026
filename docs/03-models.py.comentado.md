# models.py - Arquivo comentado

## 1. Importações

```python
from django.db import models
from .normalizacao import (
    limpar_texto,
    normalizar_bairro,
    normalizar_cep,
    normalizar_cnpj,
    normalizar_data,
    normalizar_telefone,
)
```

- `django.db import models` → importa as classes utilizadas para definir modelos e campos no Django;
- `.normalizacao` → importa as funções responsáveis pelo tratamento e padronização dos dados antes do armazenamento no banco SQLite.

---

## 2. Geração automática do ID do Cliente

```python
def _gerar_proximo_id_cliente():
    ultimo = Cliente.objects.order_by("-id_cliente").first()
    if not ultimo or not ultimo.id_cliente:
        return "CLI0001"

    digitos = "".join(
        ch for ch in str(ultimo.id_cliente) if ch.isdigit()
    )

    proximo_num = (
        (int(digitos) + 1)
        if digitos
        else (Cliente.objects.count() + 1)
    )

    return f"CLI{proximo_num:04d}"
```

- `_gerar_proximo_id_cliente()` → gera identificadores personalizados para os clientes, como `CLI0001`, `CLI0002` e `CLI0003`;
- `order_by("-id_cliente").first()` → recupera o cliente com o maior identificador em ordem decrescente;
- `isdigit()` → extrai os caracteres numéricos do identificador;
- `proximo_num` → incrementa o número encontrado ou utiliza a quantidade de clientes cadastrados como alternativa;
- `f"CLI{proximo_num:04d}"` → formata o identificador com o prefixo `CLI` e pelo menos quatro dígitos.

---

## 3. Modelo Vendedor

```python
class Vendedor(models.Model):
    id_vendedor = models.AutoField(primary_key=True)
    nome_vendedor = models.CharField(max_length=255)
```

- `Vendedor` → representa os vendedores cadastrados no sistema;
- `id_vendedor` → identificador único, gerado automaticamente e utilizado como chave primária;
- `nome_vendedor` → armazena o nome do vendedor;

### Normalização do nome

```python
def save(self, *args, **kwargs):
    self.nome_vendedor = limpar_texto(
        self.nome_vendedor,
        padrao="Não informado"
    )
    super().save(*args, **kwargs)
```

- `save()` → sobrescreve o método padrão de salvamento do Django;
- `limpar_texto()` → remove espaços desnecessários e trata valores ausentes;
- `padrao="Não informado"` → define o valor utilizado quando o nome não contém informação válida;
- `super().save()` → executa o salvamento do registro no banco de dados.

### Representação textual

```python
def __str__(self):
    return self.nome_vendedor
```

- `__str__()` → permite exibir o nome do vendedor no painel administrativo do Django e nos campos de seleção.

---

## 4. Modelo Cliente

```python
class Cliente(models.Model):
```

- Representa os clientes cadastrados na distribuidora.

### Identificação e dados empresariais

```python
id_cliente = models.CharField(
    primary_key=True,
    max_length=50,
    blank=True
)

razao_social = models.CharField(
    max_length=255,
    blank=True,
    default="Não informado"
)

cnpj_normalizado = models.CharField(
    max_length=14,
    blank=True,
    default=""
)
```

- `id_cliente` → chave primária textual, preenchida automaticamente pelo método `save()` quando não informada;
- `razao_social` → nome empresarial do cliente, permitindo valores em branco e utilizando `"Não informado"` como padrão;
- `cnpj_normalizado` → armazena o CNPJ sem caracteres especiais, com limite de 14 caracteres;
- `blank=True` → permite que o campo seja deixado em branco durante a validação.

### Contato

```python
telefone_normalizado = models.CharField(
    max_length=20,
    null=True,
    blank=True
)

email = models.EmailField(
    null=True,
    blank=True
)
```

- `telefone_normalizado` → armazena o telefone do cliente após a normalização;
- `email` → armazena o endereço eletrônico do cliente;
- `EmailField` → disponibiliza validação de formato de e-mail;
- `null=True, blank=True` → permite que os campos não sejam informados.

### Endereço

```python
bairro_normalizado = models.CharField(
    max_length=100,
    blank=True,
    default="Não informado"
)

cep_normalizado = models.CharField(
    max_length=8,
    null=True,
    blank=True
)
```

- `bairro_normalizado` → armazena o bairro do cliente, permitindo valores em branco e utilizando `"Não informado"` como padrão;
- `cep_normalizado` → armazena o CEP padronizado, com até oito caracteres;
- O CEP é opcional e pode receber `NULL`.

### Data de cadastro

```python
data_cadastro_normalizado = models.DateField(
    null=True,
    blank=True
)
```

- `data_cadastro_normalizado` → armazena a data de cadastro do cliente;
- `DateField` → representa uma data sem informação de horário;
- `null=True, blank=True` → permite que a data não seja informada.

---

## 5. Relacionamento Cliente e Vendedor

```python
vendedor = models.ForeignKey(
    Vendedor,
    on_delete=models.PROTECT,
    related_name="clientes",
    null=True,
    blank=True,
)
```

- `ForeignKey(Vendedor)` → estabelece um relacionamento de um para muitos (1:N) entre Vendedor e Cliente;
- Um vendedor pode estar associado a vários clientes;
- `on_delete=models.PROTECT` → impede a exclusão de vendedores que possuem clientes vinculados;
- `related_name="clientes"` → permite consultar os clientes associados utilizando `vendedor.clientes.all()`;
- `null=True, blank=True` → permite cadastrar clientes sem vendedor associado.

**Cardinalidade:**

- **Vendedor (0,N)** → pode possuir nenhum ou vários clientes;
- **Cliente (0,1)** → pode estar associado a nenhum ou a um vendedor.

---

## 6. Normalização dos dados do Cliente

O método `save()` foi sobrescrito para padronizar os dados antes de armazená-los no SQLite.

### Geração do identificador

```python
def save(self, *args, **kwargs):
    if not limpar_texto(self.id_cliente, padrao=""):
        self.id_cliente = _gerar_proximo_id_cliente()
    else:
        self.id_cliente = limpar_texto(self.id_cliente)
```

- Verifica se o identificador do cliente foi informado;
- Caso esteja vazio, gera um novo ID utilizando `_gerar_proximo_id_cliente()`;
- Caso exista, remove espaços desnecessários utilizando `limpar_texto()`.

### Normalização dos campos

```python
self.razao_social = limpar_texto(
    self.razao_social,
    padrao="Não informado"
)

self.cnpj_normalizado = normalizar_cnpj(
    self.cnpj_normalizado
)

self.telefone_normalizado = normalizar_telefone(
    self.telefone_normalizado
)

self.email = limpar_texto(
    self.email,
    padrao=""
) or None

self.bairro_normalizado = normalizar_bairro(
    self.bairro_normalizado
)

self.cep_normalizado = normalizar_cep(
    self.cep_normalizado
)

self.data_cadastro_normalizado = normalizar_data(
    self.data_cadastro_normalizado
)

super().save(*args, **kwargs)
```

**Funções utilizadas:**

| Função | Responsabilidade |
|---|---|
| `limpar_texto()` | Remove espaços e trata valores ausentes |
| `normalizar_cnpj()` | Remove caracteres não numéricos do CNPJ |
| `normalizar_telefone()` | Padroniza os dígitos do telefone |
| `normalizar_bairro()` | Padroniza os bairros por similaridade textual |
| `normalizar_cep()` | Padroniza e verifica a estrutura do CEP |
| `normalizar_data()` | Converte diferentes formatos de data |

## 7. Representação textual do Cliente

```python
def __str__(self):
    return self.razao_social
```

- Retorna a razão social cadastrada, facilitando sua identificação no painel administrativo;

---
