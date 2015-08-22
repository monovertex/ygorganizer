
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from ygo_cards.models import (CardType, MonsterType, MonsterAttribute, Rarity,
                              CardStatus, SpellTrapProperty, CardSet)
from ygo_cards.serializers import (CardTypeSerializer, MonsterTypeSerializer,
                                   MonsterAttributeSerializer,
                                   RaritySerializer, CardStatusSerializer,
                                   SpellTrapPropertySerializer,
                                   CardSetSerializer)
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.core.cache import cache


class LoginRequiredMixin(object):

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return ensure_csrf_cookie(login_required(view))


class BootstrapDataMixin(object):

    CACHE_KEY = 'boostrap_data'

    def bootstrap(self):

        cache_data = cache.get(self.CACHE_KEY)

        if cache_data is not None:
            self._bootstrap = cache_data

        try:
            return self._bootstrap
        except:

            bootstrap_meta = {
                'cardTypes': {
                    'model': CardType,
                    'serializer': CardTypeSerializer
                },
                'monsterTypes': {
                    'model': MonsterType,
                    'serializer': MonsterTypeSerializer
                },
                'monsterAttributes': {
                    'model': MonsterAttribute,
                    'serializer': MonsterAttributeSerializer
                },
                'rarities': {
                    'model': Rarity,
                    'serializer': RaritySerializer
                },
                'cardStatuses': {
                    'model': CardStatus,
                    'serializer': CardStatusSerializer
                },
                'spellTrapProperties': {
                    'model': SpellTrapProperty,
                    'serializer': SpellTrapPropertySerializer
                },
                'cardSets': {
                    'model': CardSet,
                    'serializer': CardSetSerializer
                }
            }

            bootstrap = {}

            for key, meta in bootstrap_meta.iteritems():
                queryset = meta['model'].objects.all()
                bootstrap[key] = meta['serializer'](queryset, many=True).data

            self._bootstrap = json.dumps(
                bootstrap, cls=DjangoJSONEncoder, indent=2)
            cache.set(self.CACHE_KEY, self._bootstrap)

        return self._bootstrap
