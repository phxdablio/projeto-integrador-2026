
# settings.py — Arquivo Comentado

## 1. Diretório principal

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
```

- `Path` → permite manipular caminhos de arquivos e diretórios.
- `BASE_DIR` → identifica o diretório raiz do projeto, utilizado para localizar arquivos como o banco de dados SQLite.

---

## 2. Configurações de segurança

```python
SECRET_KEY = 'chave_secreta_do_projeto'
DEBUG = True
ALLOWED_HOSTS = []
```

- `SECRET_KEY` → chave utilizada pelo Django em mecanismos de segurança e assinatura criptográfica.
- `DEBUG=True` → habilita informações detalhadas de erros durante o desenvolvimento.
- `ALLOWED_HOSTS` → define os domínios autorizados a acessar a aplicação.

---

## 3. Aplicações instaladas

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'distribuidora',
    'rest_framework',
    'drf_spectacular',
    'rest_framework.authtoken',
]
```

**Principais aplicações:**

- `distribuidora` → aplicação responsável pelo gerenciamento de clientes e vendedores.
- `rest_framework` → disponibiliza os recursos para construção da API REST.
- `drf_spectacular` → gera o esquema OpenAPI e permite disponibilizar a documentação da API.
- `rest_framework.authtoken` → habilita o sistema de autenticação por token do DRF.
- `django.contrib.*` → aplicações nativas do Django para administração, autenticação, sessões e outros recursos.

---

## 4. Configurações do Django REST Framework

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_SCHEMA_CLASS':
        'drf_spectacular.openapi.AutoSchema',
}
```

- `TokenAuthentication` → autentica requisições utilizando tokens.
- `SessionAuthentication` → permite autenticação por sessão do Django.
- `IsAuthenticatedOrReadOnly` → permite consultas públicas e restringe operações de escrita a usuários autenticados.
- `AutoSchema` → integra o DRF ao gerador de documentação OpenAPI.

---

## 5. Documentação da API

```python
SPECTACULAR_SETTINGS = {
    'TITLE': 'API Distribuidora Vetor',
    'DESCRIPTION': 'API REST para gerenciamento de clientes e vendedores.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'REDOC_DIST': 'https://cdn.jsdelivr.net/npm/redoc@2.5.4',
}
```

- `TITLE` → define o nome da API na documentação.
- `DESCRIPTION` → apresenta a finalidade do sistema.
- `VERSION` → identifica a versão documentada.
- `SERVE_INCLUDE_SCHEMA` → controla a inclusão da rota do próprio esquema na documentação gerada.
- `REDOC_DIST` → define a origem dos arquivos da interface ReDoc.

---

## 6. Banco de dados SQLite

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

- `DATABASES` → define os bancos de dados utilizados pelo projeto.
- `ENGINE` → configura o SQLite como sistema gerenciador de banco de dados.
- `NAME` → determina o caminho do arquivo `db.sqlite3`.

---

## 7. Configurações gerais

```python
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
```

- `ROOT_URLCONF` → indica o arquivo responsável pelas rotas principais.
- `WSGI_APPLICATION` → define a aplicação WSGI utilizada por servidores compatíveis.
- `LANGUAGE_CODE` → configura o idioma padrão da aplicação.
- `TIME_ZONE` → estabelece o fuso horário padrão como UTC.
- `USE_I18N` → habilita os recursos de internacionalização.
- `USE_TZ` → ativa o suporte a fusos horários.
- `STATIC_URL` → define o prefixo das URLs dos arquivos estáticos.

---


