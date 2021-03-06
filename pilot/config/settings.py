import os
from .secrets import *
from .pipelines import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'pipeline',
#    'djangobower',
    'apps.accounts',
    'apps.visualizations',
    'apps.jobs',
    'apps.dashboards',
    'apps.schedules',
    'apps.anonymous',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',
    'apps.accounts.middleware.CustomAuthMiddleware',
)

ROOT_URLCONF = 'urls.root'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + '/templates'],
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

WSGI_APPLICATION = 'pilot.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': PG_DATABASE,
        'USER': PG_USERNAME,
        'PASSWORD': PG_PASSWORD,
        'HOST': PG_HOST,
        'PORT': PG_PORT,
        'OPTIONS': {
            'options': '-c search_path=pilot'
        },
    }
}

AUTH_USER_MODEL = 'accounts.User'

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
STATICFILES_DIRS = ( os.path.join(BASE_DIR, 'assets/dev'), )
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
#    'djangobower.finders.BowerFinder',
)

STATIC_URL = '/assets/'
STATIC_ROOT = os.path.join(BASE_DIR, 'assets/pipeline')
#BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'assets/dev')
#BOWER_INSTALLED_APPS = (
#    'jquery#2.1.4',
#    'components-font-awesome#4.4',
#    'material-design-icons',
#    'bootstrap#3'
#)


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Singapore'

USE_I18N = True

USE_L10N = True

USE_TZ = True

APPEND_SLASH = True

USE_THOUSAND_SEPARATOR = True