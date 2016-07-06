from django.db import models
from ygo_core.models import Constant, Locale
from ygo_core.utils import process_string
from django.contrib.auth.models import User
from os.path import join
from easy_thumbnails.fields import ThumbnailerImageField
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile


class CardSet(models.Model):
    name = models.CharField(max_length=255, unique=True)
    requires_update = models.BooleanField(default=True)
    with_language_code = models.BooleanField(default=True)
    dirty = models.BooleanField(default=False)
    url = models.TextField(blank=True)
    cookie = models.TextField(blank=True, null=True)
    locale = models.ForeignKey(Locale, related_name='card_sources')

    def __unicode__(self):
        return '{}'.format(self.name)


class CardType(Constant):

    @staticmethod
    def find_or_create(name):
        return Constant.find_or_create(CardType, name)


class MonsterType(Constant):

    @staticmethod
    def find_or_create(name):
        return Constant.find_or_create(MonsterType, name)


class MonsterAttribute(Constant):

    @staticmethod
    def find_or_create(name):
        return Constant.find_or_create(MonsterAttribute, name)


class Rarity(Constant):

    @staticmethod
    def find_or_create(name):
        return Constant.find_or_create(Rarity, name)


class CardStatus(Constant):

    @staticmethod
    def find_or_create(name):
        return Constant.find_or_create(CardStatus, name)


class SpellTrapProperty(Constant):

    @staticmethod
    def find_or_create(name):
        return Constant.find_or_create(SpellTrapProperty, name)


def card_image_full(image, filename):
    return join('cards', 'full', filename)


def card_image_medium(image, filename):
    return join('cards', 'medium', filename)


def card_image_small(image, filename):
    return join('cards', 'small', filename)


class CardSource(models.Model):
    identifier = models.CharField(max_length=20)
    locale = models.ForeignKey(Locale, related_name='card_sources')
    card_set = models.ForeignKey(CardSet, related_name='card_sources')

    class Meta:
        unique_together = ('identifier', 'locale', )


class Card(models.Model):
    identifier = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255, null=True, blank=True)
    card_type = models.ForeignKey(CardType, related_name='cards', null=True,
                                  blank=True)

    spell_trap_property = models.ForeignKey(SpellTrapProperty,
                                            related_name='cards', null=True,
                                            blank=True)

    monster_attribute = models.ForeignKey(MonsterAttribute,
                                          related_name='cards',
                                          null=True, blank=True)
    monster_level = models.IntegerField(null=True, blank=True)
    monster_attack = models.CharField(max_length=10, null=True, blank=True)
    monster_defense = models.CharField(max_length=10, null=True, blank=True)

    image = ThumbnailerImageField(
        upload_to=card_image_full,
        null=True, blank=True,
        resize_source=dict(size=(250, 250), crop='scale'))
    image_medium = ThumbnailerImageField(
        upload_to=card_image_medium,
        null=True, blank=True,
        resize_source=dict(size=(200, 200), crop='scale'))
    image_small = ThumbnailerImageField(
        upload_to=card_image_small,
        null=True, blank=True,
        resize_source=dict(size=(100, 100), crop='scale'))

    search_text = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.search_text = ' '.join([
            '' if self.number is None else self.number,
            '' if self.name is None else self.name,
            '' if self.description is None else self.description
        ])

        super(Card, self).save(*args, **kwargs)

    def set_image(self, extension, image_data):
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(image_data)
        img_temp.flush()

        img_file = File(img_temp)
        name = '{}{}'.format(self.pk, extension)

        self.image.delete()
        self.image.save(name, img_file)

        self.image_medium.delete()
        self.image_medium.save(name, img_file)

        self.image_small.delete()
        self.image_small.save(name, img_file)

    @property
    def image_small_tag(self):
        try:
            return '<img src="{}" width="100" height="146" />'.format(
                self.image_small.url)
        except:
            pass

    @staticmethod
    def find_or_create(name):
        name = process_string(name)
        identifier = name.replace(' ', '_')

        try:
            card = Card.objects.get(identifier=identifier)
        except:
            card = Card.objects.create(
                identifier=identifier,
                name=name
            )

        return card


class CardMonsterType(models.Model):
    card = models.ForeignKey(Card, related_name='card_monster_types')
    monster_type = models.ForeignKey(MonsterType,
                                     related_name='card_monster_types')

    class Meta:
        unique_together = ('card', 'monster_type', )


class UserCard(models.Model):
    user = models.ForeignKey(User, related_name='user_cards')
    card = models.ForeignKey(Card, related_name='user_cards')

    want_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'card', )


class Deck(models.Model):
    user = models.ForeignKey(User, related_name='decks')
    name = models.CharField(max_length=255)

    @property
    def count(self):
        return self.deck_cards.count()

    @property
    def count_main(self):
        return self.deck_cards_main.count()

    @property
    def count_extra(self):
        return self.deck_cards_extra.count()

    @property
    def count_side(self):
        return self.deck_cards_side.count()

    @property
    def card_previews(self):
        return [x.card.image for x in
                self.deck_cards
                .order_by('?')
                .select_related('card')[:4]]

    @property
    def deck_cards_main(self):
        return self.deck_cards.filter(type='m').select_related('card')

    @property
    def deck_cards_extra(self):
        return self.deck_cards.filter(type='e').select_related('card')

    @property
    def deck_cards_side(self):
        return self.deck_cards.filter(type='s').select_related('card')


class DeckCard(models.Model):
    deck = models.ForeignKey(Deck, related_name='deck_cards')
    card = models.ForeignKey(Card, related_name='deck_cards')
    type = models.CharField(choices=(
        ('m', 'Main'),
        ('e', 'extra'),
        ('s', 'side')
    ), default='m', max_length=1)


class CardVersion(models.Model):
    card = models.ForeignKey(Card, related_name='card_versions')
    card_set = models.ForeignKey(CardSet, related_name='card_versions')
    set_number = models.CharField(max_length=15)
    rarity = models.ForeignKey(Rarity, related_name='card_versions')

    search_text = models.TextField(blank=True)

    price_low = models.FloatField(blank=True, null=True)
    price_avg = models.FloatField(blank=True, null=True)
    price_high = models.FloatField(blank=True, null=True)

    price_shift = models.FloatField(blank=True, null=True)
    price_shift_3 = models.FloatField(blank=True, null=True)
    price_shift_7 = models.FloatField(blank=True, null=True)
    price_shift_21 = models.FloatField(blank=True, null=True)
    price_shift_30 = models.FloatField(blank=True, null=True)
    price_shift_90 = models.FloatField(blank=True, null=True)
    price_shift_180 = models.FloatField(blank=True, null=True)
    price_shift_365 = models.FloatField(blank=True, null=True)

    PRICE_ATTRIBUTES = [
        'price_low', 'price_avg', 'price_high',
        'price_shift', 'price_shift_3', 'price_shift_7',
        'price_shift_21', 'price_shift_30', 'price_shift_90',
        'price_shift_180', 'price_shift_365'
    ]

    class Meta(object):
        unique_together = ('set_number', 'rarity')

    def save(self, *args, **kwargs):
        self.search_text = ' '.join([
            '' if self.set_number is None else self.set_number,
            '' if self.card_set.name is None else self.card_set.name,
            '' if self.card.search_text is None else self.card.search_text
        ])

        super(CardVersion, self).save(*args, **kwargs)

    def set_prices(self, data):

        for key, value in data.iteritems():
            try:
                setattr(self, 'price_' + key, float(value))
            except:
                pass

        self.save()

    def clear_prices(self):
        for attr in self.PRICE_ATTRIBUTES:
            setattr(self, attr, None)

        self.save()

    @property
    def price_shift_text(self):
        try:
            perc = self.price_shift * 100
            result = '{0:.2f}'.format(perc)

            if (perc > 0):
                result = '+' + result

            return result + '%'
        except:
            pass

    @staticmethod
    def find_or_create(set_number, card, card_set, rarity):
        set_number = process_string(set_number)
        rarity = Rarity.find_or_create(rarity)

        try:
            card_version = CardVersion.objects.get(set_number=set_number,
                                                   rarity=rarity)
        except:
            card_version = CardVersion.objects.create(
                card=card,
                set_number=set_number,
                card_set=card_set,
                rarity=rarity
            )

        return card_version


class UserCardVersion(models.Model):
    user = models.ForeignKey(User, related_name='user_card_versions')
    card_version = models.ForeignKey(CardVersion,
                                     related_name='user_card_versions')
    have_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'card_version', )


class UserCardVersionStatistics(models.Model):
    user = models.OneToOneField(User, primary_key=True,
                                on_delete=models.DO_NOTHING)
    count = models.PositiveIntegerField(default=0)
    price_low = models.FloatField(blank=True, null=True)
    price_avg = models.FloatField(blank=True, null=True)
    price_high = models.FloatField(blank=True, null=True)
    price_shift = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False

    # View query:
    # SELECT
    #     ucv.user_id AS `user_id`,
    #     SUM(ucv.have_count) AS `count`,
    #     SUM(ucv.have_count * cv.price_shift) AS `price_shift`,
    #     SUM(ucv.have_count * cv.price_low) AS `price_low`,
    #     SUM(ucv.have_count * cv.price_avg) AS `price_avg`,
    #     SUM(ucv.have_count * cv.price_high) AS `price_high`
    # FROM `ygo_cards_cardversion` `cv`
    # LEFT JOIN `ygo_cards_usercardversion` `ucv` ON `cv`.`id` = `ucv`.`card_version_id`
    # WHERE ucv.have_count > 0
    # GROUP BY ucv.user_id