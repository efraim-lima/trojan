import os
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'your_secret_key'

DEBUG = True

ALLOWED_HOSTS = []


# Configurar as variáveis de ambiente para o Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")  # Substitua "seu_projeto" pelo nome do seu projeto Django

# Inicializar o Django
django.setup()

# Agora você pode importar os modelos corretamente
from seu_app.models import Day, KeywordsData  # Substitua "seu_app" pelo nome do seu aplicativo Django

# Configurações do banco de dados MongoDB
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'your_database_name',
        'ENFORCE_SCHEMA': True,
        'CLIENT': {
            'host': 'mongodb://localhost',
            'port': '27017',
            'username': 'your_username',
            'password': 'your_password',
            'authSource': 'your_auth_database',  # Opcional: substitua pelo banco de dados de autenticação desejado
            'authMechanism': 'SCRAM-SHA-256',  # Ou 'MONGODB-CR' se necessário
        }
    }
}

# Configurações de aplicativos
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'trojan',  # Substitua pelo nome do seu aplicativo
]

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'your_project_name.urls'  # Substitua pelo nome do seu projeto

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'your_project_name.wsgi.application'  # Substitua pelo nome do seu projeto

# Configurações de autenticação
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

# Resto das configurações específicas do seu projeto...
