from __future__ import absolute_import

from celery import shared_task
from ygo_cards.models import (Card, CardType, MonsterType, MonsterAttribute,
                              CardStatus, SpellTrapProperty, CardMonsterType)
from ygo_variables.models import Variable
from ygo_core.utils import process_string
from pyquery import PyQuery as pq
from os.path import basename, splitext
from urlparse import urlparse
import urllib2
import re
from ygo_cards.tasks.utils import output_print

WIKI_URL = Variable.objects.get(identifier='wiki-url').get()

BREAK_TOKEN = '__BREAK__'


def get_wiki_data(identifier):

    Q = pq(url=(u'{}/{}'.format(WIKI_URL, identifier)))

    card = Q('.cardtable')
    statuses = Q('.cardtablestatuses')

    data = {
        'image': (card.find('td.cardtable-cardimage').eq(0)
                  .find('img').eq(0).attr('src')),
        'type': ('trap' if card.find('img[alt="TRAP"]') else
                 ('spell' if card.find('img[alt="SPELL"]') else
                  ('monster' if card.find('th a[title="Type"]') else
                   'other'))),
        'status_advanced': (statuses.find('th a[title="Advanced Format"]')
                            .eq(0).parents('th').next().text()),
        'status_traditional': (
            statuses.find('th a[title="Traditional Format"]').eq(0)
            .parents('th').next().text())
    }

    try:
        description_element = (card.find('td table table').eq(0)
                               .find('tr').eq(2).find('td').eq(0))

        description_element.html(re.sub(r'<br ?/?>', BREAK_TOKEN,
                                        description_element.html()))

        data['description'] = process_string(description_element.text())

        data['description'] = data['description'].replace(BREAK_TOKEN, '<br />')
    except:
        data['description'] = ''

    try:
        data['number'] = process_string(card.find('th a[title="Card Number"]')
                                        .eq(0).parents('tr').eq(0).find('td a')
                                        .eq(0).text())
    except:
        data['number'] = ''

    if (data['type'] == 'monster'):
        data['monster_attribute'] = (card.find('th a[title="Attribute"]')
                                     .eq(0).parents('tr').eq(0)
                                     .find('td a').eq(0).text())

        try:
            data['monster_level'] = int(process_string(
                card.find('th a[title="Level"]').eq(0).parents('tr').eq(0)
                .find('td a').eq(0).text()))
        except:
            data['monster_level'] = int(process_string(
                card.find('th a[title="Rank"]').eq(0).parents('tr').eq(0)
                .find('td a').eq(0).text()))

        atk_def = (card.find('th a[title="ATK"]').eq(0)
                   .parents('tr').eq(0).find('td').eq(0).text()).split('/')

        data['monster_attack'] = process_string(atk_def[0])
        data['monster_defense'] = process_string(atk_def[1])

        data['monster_types'] = (process_string(
            card.find('th a[title="Type"]').eq(0).parents('tr').eq(0)
            .find('td').eq(0).text())).split('/')

    elif (data['type'] == 'spell' or data['type'] == 'trap'):
        data['spell_trap_property'] = (
            card.find('th a[title="Property"]').eq(0).parents('tr').eq(0)
            .find('td a').eq(0).text())

    return data


@shared_task
def fetch_cards(output=output_print):
    limit = Variable.objects.get(identifier='fetch-cards-max').get()
    cards = Card.objects.filter(requires_update=True)[:limit]

    if len(cards):
        for card in cards:
            identifier = card.identifier

            output(u'Fetching card {}: {}'.format(card.id, card.name))

            try:
                data = get_wiki_data(identifier)
            except:

                try:
                    identifier = card.card_versions.all()[0].set_number
                    data = get_wiki_data(identifier)
                except:
                    identifier = card.number
                    data = get_wiki_data(identifier)

            card.description = data['description']
            card.card_type = CardType.find_or_create(data['type'])
            card.number = data['number']
            card.status_traditional = CardStatus.find_or_create(
                data['status_traditional'])
            card.status_advanced = CardStatus.find_or_create(
                data['status_advanced'])

            try:
                filename, file_extension = splitext(basename(urlparse(
                    data['image']).path))

                card.set_image(file_extension,
                               urllib2.urlopen(data['image']).read())
            except:
                pass

            if (data['type'] == 'monster'):
                card.monster_attribute = MonsterAttribute.find_or_create(
                    data['monster_attribute'])
                card.monster_level = data['monster_level']
                card.monster_attack = data['monster_attack']
                card.monster_defense = data['monster_defense']

                card.card_monster_types.all().delete()
                for monster_type in data['monster_types']:
                    CardMonsterType.objects.create(
                        card=card,
                        monster_type=MonsterType.find_or_create(
                            monster_type)
                    )
            elif (data['type'] == 'spell' or data['type'] == 'trap'):
                card.spell_trap_property = (
                    SpellTrapProperty.find_or_create(
                        data['spell_trap_property']))

            card.requires_update = False
            card.save()

            del data
