
# admin.py — Arquivo Comentado

## 1. Importações

```python
from django.contrib import admin
from .models import Cliente, Vendedor
```

- `admin` → disponibiliza os recursos do painel administrativo do Django.
- `Cliente` e `Vendedor` → modelos que serão gerenciados pelo painel.

---

## 2. Administração de Vendedores

```python
@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = ('id_vendedor', 'nome_vendedor')
    search_fields = ('nome_vendedor',)
    ordering = ('nome_vendedor',)
```

- `@admin.register(Vendedor)` → registra a entidade no painel administrativo.
- `list_display` → exibe o identificador e o nome do vendedor.
- `search_fields` → habilita pesquisas pelo nome.
- `ordering` → organiza os registros alfabeticamente.

---

## 3. Administração de Clientes

```python
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        'id_cliente',
        'razao_social',
        'cnpj_normalizado',
        'telefone_normalizado',
        'email',
        'bairro_normalizado',
        'vendedor',
    )

    search_fields = (
        'razao_social',
        'cnpj_normalizado',
        'email',
    )

    list_filter = (
        'bairro_normalizado',
        'vendedor',
        'data_cadastro_normalizado',
    )

    ordering = ('razao_social',)
    list_select_related = ('vendedor',)
```

- `list_display` → apresenta as principais informações dos clientes.
- `search_fields` → permite pesquisar por razão social, CNPJ ou e-mail.
- `list_filter` → disponibiliza filtros por bairro, vendedor e data.
- `ordering` → organiza os clientes por razão social.
- `list_select_related` → otimiza a recuperação dos vendedores associados.

---

O painel administrativo está disponível na rota `/admin/`
e exige autenticação de um usuário com permissão de acesso.
