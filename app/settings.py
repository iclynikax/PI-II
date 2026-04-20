from pathlib import Path
from decouple import config
import os
from django.contrib.messages import constants


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-u#p&fcmkx%e)mb-3=kr(po)01r$02j9$z_(ps#(4de+a9j6nuf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False

ALLOWED_HOSTS = ['iclynikax.construplus.net/''construplus.net/iclynikax', "*"]


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'usuarios',
    'medico',
    'paciente',
    'security',
]
INSTALLED_APPS += ['corsheaders']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware'] + MIDDLEWARE
CORS_ALLOW_ALL_ORIGINS = True  # ou configure domínios específicos

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Local que define publica as variáveis o perfil do usuário que esta logado.
                'usuarios.context_processors.perfil_usuario',
                'usuarios.context_processors.uf_estados',

            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# Acesso ao banco de Dados sql.lite - Que é o padrão do Django.
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}

# --------------------------------------------------------------------------------------------------
# Modelo para acesso ao banco de dados MySql
# Antes de instalar o pacote Python, instale os pacotes de desenvolvimento do MySQL:
# sudo apt update
# sudo apt install python3-dev default-libmysqlclient-dev build-essential
# Instalar o conector oficial da Oracle:
# pip install mysql-connector-python
#
# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'ENGINE': 'mysql.connector.django',    # conector oficial da Oracle: pip install mysql-connector-python
#        'NAME': 'nome_do_banco',               # Substitua pelo nome do seu banco de dados
#        'USER': 'usuario_mysql',               # Substitua pelo seu usuário do MySQL
#        'PASSWORD': 'senha_mysql',             # Substitua pela sua senha do MySQL
#        'HOST': 'localhost',                   # Ou o IP do servidor MySQL
#        'PORT': '3306',                        # Porta padrão do MySQL
#        'OPTIONS': {
#            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#        },
#    }
# }
# --------------------------------------------------------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        # Substitua pelo nome do seu banco de dados
        'NAME': 'iclynikax',
        'USER': 'UnivespEng',          # Substitua pelo seu usuário do MySQL
        'PASSWORD': 'PoloAda9Uni*!',   # Substitua pela sua senha do MySQL
        'HOST': '192.168.1.126',       # Ou o IP do servidor MySQL
        'PORT': '3306',                # Porta padrão do MySQL
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'pt-BR'
TIME_ZONE = 'America/Sao_Paulo'
USE_TZ = False

USE_I18N = True

# Configurações para formatar valores digitais decimais
THOUSAND_SEPARATOR = '.',
USE_THOUSAND_SEPARATOR = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'templates/static'),)
STATIC_ROOT = os.path.join('static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEFAULT_FROM_EMAIL = 'gdmacedo@gmail.com'

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST = config('EMAIL_HOST')

# Mensagens


MESSAGE_TAGS = {
    constants.DEBUG: 'alert-primary',
    constants.ERROR: 'alert-danger',
    constants.SUCCESS: 'alert-success',
    constants.INFO: 'alert-info',
    constants.WARNING: 'alert-warning',
}

# chaves de acesso a API do Google Maps
GOOGLE_MAPS_KEY = config("Key_Google_Maps")
