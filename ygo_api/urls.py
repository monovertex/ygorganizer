from django.conf.urls import patterns, url
from .views import (
    UserCardVersionView, BrowseView, CollectionView,
    UserCardView, DeckViewSet, CardViewSet)
from rest_framework import routers


router = routers.DefaultRouter(trailing_slash=True)
router.register(r'decks', DeckViewSet)
router.register(r'cards', CardViewSet)

urlpatterns = router.urls

urlpatterns += patterns(
    '',
    url(r'^user-card-version/$', UserCardVersionView.as_view(),
        name='api_user_card_version'),
    url(r'^user-card/$', UserCardView.as_view(), name='api_user_card'),

    url(r'^browse/$', BrowseView.as_view(), name='api_browse'),
    url(r'^collection/$', CollectionView.as_view(), name='api_collection'),
)
