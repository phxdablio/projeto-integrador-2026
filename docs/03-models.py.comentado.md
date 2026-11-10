
# models.py - Arquivo comentado

```python
from django.db import models
```

- `django.db import models` → importa as classes utilizadas para definir modelos e campos no Django;
- Cada modelo representa uma entidade que será armazenada no banco de dados (SQLite).

### Modelo Vendedor

```python
class Vendedor(models.Model):
```

- Representa os vendedores responsáveis pelos clientes cadastrados no sistema.

```python
id_vendedor = models.AutoField(primary_key=True)
nome_vendedor = models.CharField(max_length=255)
```

- `id_vendedor` → identificador único de cada vendedor, gerado automaticamente e chave primária da tabela do banco de dados;
- `nome_vendedor` → armazena o nome do vendedor.

```python
def __str__(self):
    return self.nome_vendedor
```

- Permite exibir o nome do vendedor no painel administrativo do Django e no shell.

### Modelo/Tabela Cliente

```python
class Cliente(models.Model):
```

- Representa os clientes cadastrados na distribuidora.

```python
id_cliente = models.AutoField(primary_key=True)
razao_social = models.CharField(max_length=255)
cnpj_normalizado = models.CharField(max_length=14)
```

- `id_cliente` → identificador único de cada cliente, gerado automaticamente e chave primária da tabela do banco de dados;
- `razao_social` → nome empresarial do cliente;
- `cnpj_normalizado` → armazena o CNPJ como texto.

```python
telefone_normalizado = models.CharField(
    max_length=20, null=True, blank=True
)

email = models.EmailField(
    null=True, blank=True
)
```

- `telefone_normalizado` → armazena o telefone do cliente;
- `email` → armazena o endereço eletrônico do cliente;
- `blank=True` → permite que o campo seja deixado em branco durante a validação.

```python
bairro_normalizado = models.CharField(max_length=100)

cep_normalizado = models.CharField(
    max_length=8, null=True, blank=True
)
```

- `bairro_normalizado` → identifica o bairro do cliente;
- `cep_normalizado` → armazena o CEP do cliente;

```python
data_cadastro_normalizado = models.DateField(
    null=True, blank=True
)
```

- `data_cadastro_normalizado` → armazena a data de cadastro do cliente.
- `DateField` → representa uma data sem informação de horário.
- `null=True, blank=True` → permite que a data não seja informada.

### Relacionamento Cliente e Vendedor

```python
vendedor = models.ForeignKey(
    Vendedor,
    on_delete=models.PROTECT,
    related_name="clientes"
)
```

- `ForeignKey(Vendedor)` → estabelece um relacionamento de um para muitos (1:N) entre Vendedor e Cliente.
- Um vendedor pode estar associado a vários clientes.

**Parâmetros do relacionamento:**

- `on_delete=models.PROTECT` → impede que um vendedor seja excluído enquanto possuir clientes associados.
- `related_name="clientes"` → permite acessar todos os clientes vinculados a um vendedor utilizando `vendedor.clientes.all()`.

### Representação textual do Cliente

```python
def __str__(self):
    return self.razao_social
```

- `__str__()` → define a representação textual de cada cliente.
- Retorna a razão social cadastrada.

## Resumindo

- **Vendedor** → armazena os vendedores cadastrados na distribuidora.
- **Cliente** → armazena as informações cadastrais dos clientes.
- **Vendedor ↔ Cliente** → relacionamento 1:N.
- **ForeignKey** → associa cada cliente a um vendedor.
- **PROTECT** → impede a exclusão de vendedores que possuam clientes vinculados.
- **related_name="clientes"** → permite consultar os clientes de um vendedor.
- **SQLite** → banco de dados utilizado para armazenar as entidades e seus relacionamentos.

