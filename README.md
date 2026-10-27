# 📘 DevLab Project API

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0+-2BA977?logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-009FD4?logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-F5C518?logoColor=black)

---

## Instituições de Fomento e Parceria

[![Website IFB](https://img.shields.io/badge/Website-IFB-45B06B?labelColor=E54854&logoColor=white)](https://www.ifb.edu.br/)\
[![Website ihwbr](https://img.shields.io/badge/Website-ihwbr-FFC107?labelColor=555555&logoColor=black)](https://ihwbr.com/)

## Orientador

**Prof. Diego Martins de Oliveira**\
Github: (https://github.com/diegomoliveiraprof)

## Sumário

**(...)**

## Visão geral

Este projeto implementa uma API REST em Django (Django REST Framework) para consulta, gestão e disponibilização dos dados de clientes e vendedores da Distribuidora Vetor, previamente tratados e normalizados via pipeline de ETL.

O sistema organiza o acesso aos dados cadastrais e operacionais, estabelecendo regras de permissão e autenticação bem definidas:

&bull; **Usuário Autenticado (logado via Token) &#8594;** possui permissão total de gerenciamento (CRUD completo: criar, listar, detalhar, atualizar e excluir clientes e vendedores).

&bull; **Usuário Público (não autenticado) &#8594;** permissão somente de leitura (GET), podendo apenas consultar e filtrar registros.

### Funcionalidades principais

&bull; **CRUD Completo de Clientes:** gerenciamento dos dados cadastrais (Razão Social, CNPJ, telefone, e-mail, bairro, CEP e data de cadastro devidamente normalizados).

&bull; **CRUD Completo de Vendedores**: gerenciamento e vinculação da equipe comercial aos seus respectivos clientes.

&bull; **Consultas e Relacionamentos Especializados:**

&#8594; Listagem e agrupamento de clientes por bairro normalizado.

&#8594; Listagem de clientes atendidos por cada vendedor.

&bull; **Autenticação Segura:** emissão e validação de tokens via DRF Token Authentication *(/api/auth/token/)*.

&bull; **Painel Administrativo:** interface nativa do Django Admin configurada para auditoria e controle interno das tabelas.

&bull; **Documentação Interativa:** schema OpenAPI gerado via drf-spectacular com visualização interativa em Swagger e Redoc *(/api/docs/)*.

## Pacotes utilizados

| Pacote | Versão | Descrição |
| :--- | :---: | :--- |
| **Django** | `6.1.2` | Framework web principal |
| **djangorestframework** | `3.18.3` | Toolkit para construção da API REST |
| **drf-spectacular** | `0.30.0` | Geração automática de documentação OpenAPI (Swagger/Redoc) |
| **pandas** | `3.1.0` | Manipulação, limpeza e transformação de dados no pipeline de ETL |
| **numpy** | `2.5.4` | Operações matemáticas e suporte numérico para análise de dados |
| **python-dateutil** | `3.0.0` | Tratamento e padronização de formatos de datas inconsistentes |
| **PyYAML** | `6.0.3` | Suporte à serialização e exportação de schemas OpenAPI em YAML |
| **sqlparse** | `0.6.0` | Parsing e formatação de consultas SQL pelo Django |
| **asgiref** | `3.13.0` | Suporte assíncrono padrão (ASGI) para o Django |

## Estrutura do projeto

**(...)**
