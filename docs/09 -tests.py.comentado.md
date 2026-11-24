
# tests.py — Arquivo Comentado

## 1. Importações

```python
from django.test import TestCase
from .models import Vendedor
from .serializers import ClienteSerializer, VendedorSerializer
```

- `TestCase` → classe do Django utilizada para executar testes automatizados em um banco de dados isolado.
- `Vendedor` → modelo utilizado para criar vendedores durante os testes.
- `ClienteSerializer` e `VendedorSerializer` → serializers submetidos aos testes de validação.

---

## 2. Testes do VendedorSerializer

```python
class VendedorSerializerTest(TestCase):
```

- Define a classe responsável por verificar a validação dos dados dos vendedores.

### Teste 1 — Vendedor válido

```python
def test_vendedor_valido(self):
    dados = {
        "nome_vendedor": "Carlos Silva"
    }

    serializer = VendedorSerializer(data=dados)

    self.assertTrue(serializer.is_valid())
```

**Objetivo:** verificar se o serializer aceita um vendedor com nome válido.

**Resultado esperado:**
- `serializer.is_valid()` → `True`.
- `serializer.errors` → `{}` (sem erros de validação).
- **Status:** APROVADO, caso os dados sejam aceitos.

### Teste 2 — Vendedor sem nome

```python
def test_vendedor_sem_nome(self):
    dados = {}

    serializer = VendedorSerializer(data=dados)

    self.assertFalse(serializer.is_valid())

    self.assertIn(
        "nome_vendedor",
        serializer.errors
    )
```

**Objetivo:** verificar se o serializer rejeita o cadastro de um vendedor sem nome.

**Resultado esperado:**
- `serializer.is_valid()` → `False`.
- `serializer.errors` → contém o campo `nome_vendedor`.
- Mensagem esperada: `This field is required.`
- **Status:** APROVADO, caso o erro seja identificado.

---

## 3. Testes do ClienteSerializer

```python
class ClienteSerializerTest(TestCase):
```

- Define a classe responsável pelos testes de validação dos clientes.

### Preparação dos dados — setUp()

```python
def setUp(self):
    self.vendedor = Vendedor.objects.create(
        nome_vendedor="Carlos Silva"
    )

    self.dados = {
        "razao_social": "Empresa Exemplo LTDA",
        "cnpj_normalizado": "12345678000195",
        "telefone_normalizado": "61999999999",
        "email": "empresa@exemplo.com",
        "bairro_normalizado": "Asa Norte",
        "cep_normalizado": "70000000",
        "data_cadastro_normalizado": "2026-11-04",
        "vendedor": self.vendedor.id_vendedor
    }
```

- `setUp()` → executado antes de cada teste da classe.
- `Vendedor.objects.create()` → cria um vendedor no banco de testes.
- `self.dados` → define um conjunto de informações válidas para testar o cadastro de clientes.

### Teste 3 — Cliente válido

```python
def test_cliente_valido(self):
    serializer = ClienteSerializer(data=self.dados)

    self.assertTrue(
        serializer.is_valid(),
        serializer.errors
    )
```

**Objetivo:** verificar se o serializer aceita os dados de um cliente válido.

**Resultado esperado:**
- `serializer.is_valid()` → `True`.
- `serializer.errors` → `{}`.
- Os dados atendem às validações definidas no modelo.
- **Status:** APROVADO, caso não sejam identificados erros.

### Teste 4 — Cliente com e-mail inválido

```python
def test_cliente_email_invalido(self):
    dados = self.dados.copy()
    dados["email"] = "email_invalido"

    serializer = ClienteSerializer(data=dados)

    self.assertFalse(serializer.is_valid())

    self.assertIn(
        "email",
        serializer.errors
    )
```

**Objetivo:** verificar se o serializer rejeita um endereço de e-mail com formato inválido.

**Resultado esperado:**
- `serializer.is_valid()` → `False`.
- `serializer.errors` → contém o campo `email`.
- Mensagem esperada: `Enter a valid email address.`
- **Status:** APROVADO, caso o erro seja identificado.

### Teste 5 — Cliente sem razão social

```python
def test_cliente_sem_razao_social(self):
    dados = self.dados.copy()
    dados.pop("razao_social")

    serializer = ClienteSerializer(data=dados)

    self.assertFalse(serializer.is_valid())

    self.assertIn(
        "razao_social",
        serializer.errors
    )
```

**Objetivo:** verificar se o serializer impede o cadastro de clientes sem razão social.

**Resultado esperado:**
- `serializer.is_valid()` → `False`.
- `serializer.errors` → contém o campo `razao_social`.
- Mensagem esperada: `This field is required.`
- **Status:** APROVADO, caso a ausência seja identificada.

---

## 4. Execução dos testes

Para executar os testes da aplicação `distribuidora`, utilize:

```bash
python manage.py test distribuidora
```

**Exemplo de saída esperada:**

```text
Found 5 test(s).
Creating test database for alias 'default'...
System check identified no issues.
.....
----------------------------------------------------------------------
Ran 5 tests in 0.XXXs

OK
Destroying test database for alias 'default'...
```

- `Found 5 test(s)` → indica que cinco testes foram identificados.
- `.....` → cada ponto representa um teste aprovado.
- `OK` → indica que todos os testes foram concluídos com sucesso.

---
