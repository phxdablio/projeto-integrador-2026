# 📘 Projeto API - Primora

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

**&bull; [Visão Geral](#visão-geral)**

**&bull; [Pacotes Utilizados](#pacotes-utilizados)**

**&bull; [Estrutura do Projeto](#estrutura-do-projeto)**

**&bull; [Diagrama de Banco de Dados](#diagrama-de-banco-de-dados)**

**&bull; [Documentação API](#documentação-api)**

**&bull; [Configuração do Ambiente](#configuração-do-ambiente)**

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

```bash
projeto_api/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── clientes/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── admin.py
│   ├── tests.py
│   └── migrations/
├── vendedores/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── admin.py
│   ├── tests.py
│   └── migrations/
└── docs/
    └── database_diagram.png
```

&bull; **config/ →** configurações principais do Django, incluindo banco de dados, autenticação e rotas globais da API.

&bull; **clientes/ →** aplicação responsável pelo cadastro, consulta, atualização e exclusão de clientes, além dos filtros por bairro e vendedor.

&bull; **vendedores/ →** aplicação responsável pelo gerenciamento de vendedores e pela consulta de seus respectivos clientes.

&bull; **db.sqlite3 →** arquivo do banco de dados SQLite que armazena os registros.

&bull; **docs/ →** documentação auxiliar do projeto, incluindo o Diagrama Entidade-Relacionamento (DER).


## Diagrama de banco de dados

## Diagrama ER 
### Cliente

| Campo | Tipo | Descrição |
|---|---|---|
| id_cliente | PK (int) | Identificador único do cliente |
| razao_social | CharField | Razão social do cliente |
| cnpj_normalizado | CharField | CNPJ do cliente, sem caracteres especiais |
| telefone_normalizado | CharField | Telefone do cliente em formato padronizado |
| email | EmailField | Endereço de e-mail do cliente |
| bairro_normalizado | CharField | Bairro do cliente em formato padronizado |
| cep_normalizado | CharField | CEP do cliente, sem caracteres especiais |
| data_cadastro_normalizado | DateField | Data de cadastro do cliente |
| vendedor_id | FK (int) | Identificador do vendedor responsável pelo cliente |

### Vendedor

| Campo | Tipo | Descrição |
|---|---|---|
| id_vendedor | PK (int) | Identificador único do vendedor |
| nome_vendedor | CharField | Nome do vendedor |


## Relacionamentos

- **Vendedor (1) ↔ (N) Cliente**  
  Um vendedor pode ser responsável por vários clientes, mas cada cliente está associado a um único vendedor.

---


## Representação Visual em Texto

**Entidades principais:**

- **Vendedor** → pode ser responsável por vários clientes.
- **Cliente** → possui informações cadastrais e está associado a um vendedor.

**Relacionamentos:**

- Vendedor ↔ Cliente → **1:N**

## Documentação API

A documentação interativa está disponível em:

&bull; `/api/docs/` → Swagger UI / spectacular

&bull; `/api/docs/redoc/` → ReDoc

| Método | Endpoint | Descrição | Autenticação |
|---|---|---|---|
| CRUD | `/api/clientes/` | Gerenciamento de clientes | Requerida |
| GET | `/api/clientes/{id}/` | Detalhes de um cliente específico | Requerida |
| GET | `/api/clientes/bairro/{nome}/` | Lista clientes por bairro | Requerida |
| GET | `/api/clientes/vendedor/{id}/` | Lista clientes por vendedor | Requerida |
| CRUD | `/api/vendedores/` | Gerenciamento de vendedores | Requerida |
| GET | `/api/vendedores/{id}/clientes/` | Lista clientes de um vendedor específico | Requerida |
| POST | `/api/auth/token/` | Autenticação via token | Não requerida |

## Configuração do ambiente

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/phxdablio/projeto-integrador-2026.git
   cd projeto_integrador_2026
   ```

2. **Crie um ambiente virtual:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**

   ```bash
   cp .env.example .env
   # Edite .env com suas credenciais
   ```

5. **Aplique as migrações e inicie o servidor:**
   
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

