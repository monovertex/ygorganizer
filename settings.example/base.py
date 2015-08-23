
from django.contrib.messages import constants as messages
from path.base import STATIC_DIR, TEMPLATES_DIR
from django.core.urlresolvers import reverse_lazy
from datetime import timedelta

SECRET_KEY = '<secret_key>'

ADMINS = (<admins_tuple>)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'easy_thumbnails',
    'rest_framework',
    'rest_framework_extensions',
    'registration',
    'debug_toolbar',
    'crispy_forms',

    'ygo_core',
    'ygo_variables',
    'ygo_cards',
    'ygo_api',
    'ygo_import'
)

MIDDLEWARE_CLASSES = (
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'ygo_core.urls'

SESSION_ENGINE = 'django.contrib.sessions.backends.file'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = False

WSGI_APPLICATION = 'settings.wsgi.application'

TEMPLATE_DIRS = (
    TEMPLATES_DIR,
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.media',
    'ygo_core.context_processors.settings'
)

MEDIA_URL = '/media/'

STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)

STATICFILES_DIRS = (STATIC_DIR,)

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    messages.SUCCESS: 'info'
}

LOGIN_URL = reverse_lazy('auth_login')
LOGOUT_URL = reverse_lazy('auth_logout')
LOGIN_REDIRECT_URL = reverse_lazy('collection')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

ACCOUNT_ACTIVATION_DAYS = 30
REGISTRATION_AUTO_LOGIN = True

EMAIL_HOST = '<email_host>'
EMAIL_HOST_USER = '<email_user>'
EMAIL_HOST_PASSWORD = '<email_password>'
EMAIL_USE_SSL = True
EMAIL_PORT = <email_ssl_port>
DEFAULT_FROM_EMAIL = '<email_from>'
SERVER_EMAIL = '<server_email>'

INTERNAL_IPS = ['<internal_ip>',]

CRISPY_TEMPLATE_PACK = 'bootstrap3'

HTML_MINIFY = True

CELERY_SEND_TASK_ERROR_EMAILS = True

CELERYBEAT_SCHEDULE = {
    'fetch-cards': {
        'task': 'ygo_cards.tasks.cards.fetch_cards',
        'schedule': timedelta(hours=4),
    },
    'fetch-sets': {
        'task': 'ygo_cards.tasks.sets.fetch_sets',
        'schedule': timedelta(hours=1),
    },
}

CELERY_TIMEZONE = 'UTC'
