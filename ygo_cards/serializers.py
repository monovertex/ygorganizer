from rest_framework import serializers
from ygo_core.serializers import ConstantSerializer
from .models import (CardType, MonsterType, MonsterAttribute, Rarity,
                     CardStatus, SpellTrapProperty, Card, CardVersion,
                     CardMonsterType, UserCardVersion, CardSet, UserCard,
                     Deck, DeckCard)


class CardSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = CardSet
        fields = ('id', 'name')


class CardTypeSerializer(ConstantSerializer):

    class Meta(ConstantSerializer.Meta):
        model = CardType


class MonsterTypeSerializer(ConstantSerializer):

    class Meta(ConstantSerializer.Meta):
        model = MonsterType


class MonsterAttributeSerializer(ConstantSerializer):

    class Meta(ConstantSerializer.Meta):
        model = MonsterAttribute


class RaritySerializer(ConstantSerializer):

    class Meta(ConstantSerializer.Meta):
        model = Rarity


class CardStatusSerializer(ConstantSerializer):

    class Meta(ConstantSerializer.Meta):
        model = CardStatus


class SpellTrapPropertySerializer(ConstantSerializer):

    class Meta(ConstantSerializer.Meta):
        model = SpellTrapProperty


class CardMonsterTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CardMonsterType
        fields = ('id', 'card', 'monster_type')


class CardSerializer(serializers.ModelSerializer):

    image_medium = serializers.ImageField()
    image_small = serializers.ImageField()

    class Meta:
        model = Card
        fields = ('id', 'identifier', 'name', 'number', 'description',
                  'card_type', 'status_traditional', 'status_advanced',
                  'spell_trap_property', 'monster_attribute', 'monster_level',
                  'monster_attack', 'monster_defense', 'image', 'image_medium',
                  'image_small')


class UserCardVersionSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCardVersion
        fields = ('id', 'user', 'card_version', 'have_count',)


class UserCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCard
        fields = ('id', 'user', 'card', 'want_count',)


class DeckCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeckCard
        fields = ('id', 'deck', 'card', 'type',)


class CardVersionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CardVersion
        fields = ('id', 'card_set', 'set_number', 'rarity',
                  'price_low', 'price_avg', 'price_high', 'card',
                  'price_shift_text', 'price_shift')


class DeckSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deck
        fields = ('id', 'user', 'name', 'deck_cards',

                  'count', 'count_main', 'count_extra', 'count_side',

                  'card_previews',

                  'deck_cards_main', 'deck_cards_extra', 'deck_cards_side')
        read_only_fields = ('id', 'user')


class DeckCardSerializerFull(serializers.ModelSerializer):

    card = CardSerializer()

    class Meta(DeckCardSerializer.Meta):
        pass


class DeckSerializerFull(DeckSerializer):

    card_previews = serializers.ListField(
        child=serializers.ImageField(),
        read_only=True
    )

    deck_cards = DeckCardSerializerFull(many=True)
    deck_cards_main = DeckCardSerializerFull(many=True, read_only=True)
    deck_cards_extra = DeckCardSerializerFull(many=True, read_only=True)
    deck_cards_side = DeckCardSerializerFull(many=True, read_only=True)

    class Meta(DeckSerializer.Meta):
        pass


class CardSerializerFull(CardSerializer):
    card_monster_types = CardMonsterTypeSerializer(many=True)
    card_versions = CardVersionSerializer(many=True)

    class Meta(CardSerializer.Meta):
        fields = CardSerializer.Meta.fields + (
            'card_versions', 'card_monster_types')
        lookup_field = 'identifier'


class CardVersionSerializerFull(CardVersionSerializer):
    card = CardSerializerFull()
