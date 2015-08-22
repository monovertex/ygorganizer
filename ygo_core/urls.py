from django.conf.urls import patterns, url, include
from django.contrib import admin
from .views import (CollectionPageView, BrowsePageView, AboutPageView,
                    IndexPageView, DonationsPageView)

admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'^api/', include('ygo_api.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^auth/', include('registration.backends.default.urls')),
    url(r'^import/', include('ygo_import.urls')),

    url(r'^$', IndexPageView.as_view(), name='index'),
    url(r'^about/$', AboutPageView.as_view(), name='about'),
    url(r'^donate/$', DonationsPageView.as_view(), name='donations'),

    url(r'^collection/(.+?/)?$', CollectionPageView.as_view(),
        name='collection'),
    url(r'^browse/(.+?/)?$', BrowsePageView.as_view(), name='browse'),

    # url(r'^wishlist/$', BrowsePageView.as_view(), name='wishlist'),
    # url(r'^deck-list/$', DeckListPageView.as_view(), name='decks'),
    # url(r'^deck/([0-9]+/)$', BrowsePageView.as_view(), name='deck'),
)
