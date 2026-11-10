
from django.contrib import admin
from .models import Cliente, Vendedor


@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = (
        'id_vendedor',
        'nome_vendedor',
    )

    search_fields = ('nome_vendedor',)

    ordering = ('nome_vendedor',)


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
