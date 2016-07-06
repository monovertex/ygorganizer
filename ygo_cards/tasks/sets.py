from __future__ import absolute_import

from celery import shared_task
from ygo_cards.models import Card, CardVersion, CardSet, UserCardVersion
from ygo_core.utils import process_string, slugify
from ygo_variables.models import Variable
import unirest
import urllib
import urllib2
from ygo_cards.utils import sn_has_language_code, sn_normalize
from ygo_cards.tasks.utils import output_print
import dateutil.parser
from django.db import transaction
from django.conf import settings
from pyquery import PyQuery as pq
import re


@shared_task
def fetch_sets(output=output_print):
    step = Variable.objects.get(identifier='fetch-sets-step')

    if step.get() == 0:
        output(u' ### Fetching list of sets ### ')

        # Mark all sets as dirty (inexistent) and that they require update.
        CardSet.objects.all().update(dirty=True, requires_update=True)

        # Iterate the locale links.
        for locale, url in settings.YUGIOH_DATABASE['locales'].iteritems():
            response = urllib2.urlopen(url)
            Q = pq(response.read())

            cookie_raw = response.info().getheader('Set-Cookie')
            try:
                cookie = re.findall(r'(JSESSIONID=.*?);', cookie_raw)[0]
            except:
                cookie = None

            # Select all DOM objects for sets.
            set_sources = Q('.list_body .pack')
            for set_source in set_sources.items():
                # Parse the name.
                set_name = process_string(set_source.text())

                # Parse the url.
                set_url = '{}{}'.format(
                    settings.YUGIOH_DATABASE['root'],
                    set_source.find('input[type="hidden"]').attr('value')
                )

                # Update or create the set object.
                card_set, created = CardSet.objects.get_or_create(
                    name=set_name)
                card_set.url = set_url
                card_set.dirty = False
                card_set.cookie = cookie
                card_set.save()

                output(card_set.name)

        step.set(1)
    elif step.get() == 1:
        output(u' --- Fetching individual sets --- ')

        limit = Variable.objects.get(identifier='fetch-sets-max').get()
        sets = CardSet.objects.filter(requires_update=True)[:limit]

        if len(sets):
            for card_set in sets:
                output(u'Fetching set {}...'.format(card_set.name))

                Q = pq(card_set.url, headers={
                    'Cookie': card_set.cookie
                })

                card_sources = Q('ul.box_list li')
                for card_source in card_sources.items():
                    relative_url = card_source.find(
                        'input[type="hidden"]').attr('value')
                    card_identifier = re.findall(
                        r'cid=([0-9])', relative_url)[0]
                    card_url = '{}{}'.format(
                        settings.YUGIOH_DATABASE['root'],
                        relative_url
                    )
                    card, created = Card.objects.get_or_create(
                        identifier=card_identifier)
                    card.url = card_url
                    card_set.dirty = False
                    card_set.cookie = cookie
                    card_set.save()

                    output(card_set.name)