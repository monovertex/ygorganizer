

from django.conf.urls import patterns, url
from .views import ImportView


urlpatterns = patterns(
    '',
    url(r'^(?P<step>[a-z]+)/$', ImportView.as_view(), name='import'),
    url(r'^$', ImportView.as_view(), name='import'),
)
