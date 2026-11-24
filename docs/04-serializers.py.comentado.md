
# serializers.py — Arquivo Comentado

## 1. Importações

```python
from rest_framework import serializers
from .models import Cliente, Vendedor
```

- `from rest_framework import serializers` → importa o módulo de serialização do Django;
- `from .models import Cliente, Vendedor` → importa os modelos `Cliente` e `Vendedor` definidos no arquivo `models.py`;

## 2. ClienteSerializer

```python
class ClienteSerializer(serializers.ModelSerializer):
```

- Define a classe `ClienteSerializer`, responsável pela serialização e validação dos dados dos clientes.
- Herda de `serializers.ModelSerializer`, classe do DRF que cria automaticamente os campos e validações básicas com base no modelo Django.
- Permite transformar instâncias de `Cliente` em dados serializáveis e validar informações recebidas para cadastro ou atualização.

### Configuração da classe Meta

```python
class Meta:
    model = Cliente
    fields = '__all__'
```

- `class Meta` → classe interna utilizada para configurar o comportamento do serializer.
- `model = Cliente` → associa o serializer ao modelo `Cliente`, definido no banco de dados e no models.
- `fields = '__all__'` → determina que todos os campos do modelo `Cliente` sejam incluídos na serialização.

### Funcionamento

O `ClienteSerializer` realiza duas funções principais:

1. **Serialização:** transforma instâncias do modelo `Cliente` em dados que podem ser enviados como JSON na resposta da API.
2. **Desserialização e validação:** recebe dados enviados pelo usuário, verifica as regras básicas dos campos e permite a criação ou atualização de registros.

### Validações automáticas

Por herdar de `ModelSerializer`, o serializer utiliza as restrições definidas no modelo.

Exemplos:

- `razao_social` → campo obrigatório.
- `cnpj_normalizado` → aceita até 14 caracteres.
- `email` → verifica o formato do endereço eletrônico, quando informado.
- `cep_normalizado` → aceita até 8 caracteres.
- `vendedor` → deve referenciar um vendedor existente.

## 3. VendedorSerializer

```python
class VendedorSerializer(serializers.ModelSerializer):
```

- Define a classe `VendedorSerializer`, responsável pela serialização e validação dos dados dos vendedores.
- Herda de `serializers.ModelSerializer`, aproveitando os campos e regras estabelecidos no modelo `Vendedor`.

### Configuração da classe Meta

```python
class Meta:
    model = Vendedor
    fields = '__all__'
```

- `model = Vendedor` → associa o serializer ao modelo `Vendedor`.
- `fields = '__all__'` → inclui todos os campos definidos no modelo.

**Campos contemplados:**

- `id_vendedor` → identificador único do vendedor.
- `nome_vendedor` → nome do vendedor.

### Funcionamento

O `VendedorSerializer` permite:

1. Validar os dados enviados para cadastro ou atualização.
2. Utilizar as restrições de campos estabelecidas no modelo `Vendedor`.

