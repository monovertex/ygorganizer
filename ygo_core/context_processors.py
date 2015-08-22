
from django.conf import settings as django_settings


def settings(request):

    return {
        'debug': django_settings.DEBUG,
        'GA_ID': django_settings.GA_ID
    }
