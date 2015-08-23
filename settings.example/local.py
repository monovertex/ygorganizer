
from settings.base import *
from path.local import BASE_DIR
from os.path import join

DEBUG = True

TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<database_name>',
        'USER': '<database_user>',
        'PASSWORD': '<database_password>',
        'HOST': '<database_host>',
        'PORT': ''
    }
}

ALLOWED_HOSTS = ['<local_hostname>']

MEDIA_ROOT = join(BASE_DIR, '<name_of_media_directory>')

STATIC_ROOT = join(BASE_DIR, '<name_of_static_directory>')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'KEY_PREFIX': 'ygorganizer',
    }
}

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': 'unix:<path/to/memcached/socket>',
#         'KEY_PREFIX': 'ygorganizer',
#     }
# }

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

GA_ID = '<google_analytics_id>'
