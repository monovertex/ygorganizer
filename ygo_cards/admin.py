from django.contrib import admin
from .models import (CardType, MonsterType, MonsterAttribute, Rarity,
                     CardStatus, SpellTrapProperty, Card, CardMonsterType,
                     CardVersion, UserCardVersion, CardSet, UserCard)

admin.site.register(CardSet)
admin.site.register(CardType)
admin.site.register(MonsterType)
admin.site.register(MonsterAttribute)
admin.site.register(Rarity)
admin.site.register(CardStatus)
admin.site.register(SpellTrapProperty)
admin.site.register(Card)
admin.site.register(CardMonsterType)
admin.site.register(CardVersion)
admin.site.register(UserCardVersion)
admin.site.register(UserCard)
