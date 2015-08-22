from __future__ import absolute_import

from celery import shared_task
from ygo_cards.models import Card, CardVersion, CardSet, UserCardVersion
from ygo_core.utils import process_string, slugify
from ygo_variables.models import Variable
import unirest
import urllib
from ygo_cards.utils import sn_has_language_code, sn_normalize
from ygo_cards.tasks.utils import output_print
import dateutil.parser
from django.db import transaction

API_SETS_LIST = 'http://yugiohprices.com/api/card_sets'
API_SET = 'http://yugiohprices.com/api/set_data/{}'


def combine_prices(a, b):
    if a['status'] != 'success':
        return b
    elif b['status'] != 'success':
        return a
    elif a['status'] != 'success' and b['status'] != 'success':
        return None

    a = a['data']['prices']
    b = b['data']['prices']

    preferred_source = None

    try:
        a['updated_at'] = dateutil.parser.parse(a['updated_at'])
    except:
        preferred_source = b

    try:
        b['updated_at'] = dateutil.parser.parse(b['updated_at'])
    except:
        preferred_source = a

    if preferred_source is None:
        preferred_source = (a if a['updated_at'] > b['updated_at'] else b)

    result = {
        'status': 'success',
        'data': {
            'prices': {
                'updated_at': preferred_source['updated_at']
            }
        }
    }

    for key in a:
        result_value = None

        try:
            value_a = float(a[key])
        except:
            value_a = None

        try:
            value_b = float(b[key])
        except:
            value_b = None

        if value_a is None and value_b is not None:
            result_value = value_b
        elif value_a is not None and value_b is None:
            result_value = value_a
        elif value_a is not None and value_b is not None:
            if key == 'low':
                result_value = min(value_a, value_b)
            elif key == 'high':
                result_value = max(value_a, value_b)
            else:
                result_value = float(preferred_source[key])

        result['data']['prices'][key] = result_value

    return result


@shared_task
def fetch_sets(output=output_print):
    step = Variable.objects.get(identifier='fetch-sets-step')

    # Fetch a list of sets and mark all sets for updating.
    if step.get() == 0:
        output(u' ### Fetching list of sets ### ')
        created = 0

        response = unirest.get(API_SETS_LIST)

        if response.code == 200:

            for name in response.body:
                name = process_string(name)

                try:
                    CardSet.objects.create(name=name)
                    created += 1
                except:
                    pass

            CardSet.objects.all().update(requires_update=True)

            step.set(1)

            output(u'{:d} card sets created.'.format(created))

        else:
            output(u'API call failed')

    # Fetch individual sets.
    elif step.get() == 1:
        output(u' --- Fetching individual sets --- ')
        limit = Variable.objects.get(identifier='fetch-sets-max').get()
        sets = CardSet.objects.filter(requires_update=True)[:limit]

        if len(sets):
            for card_set in sets:
                output(u'Fetching set {}...'.format(card_set.name))

                response = unirest.get(
                    API_SET.format(urllib.quote(card_set.name, '')))

                if (response.code != 200
                        or response.body['status'] != 'success'):
                    output(u'=!= Failed set {}.'.format(card_set.name))

                card_set.with_language_code = True

                for card_source in response.body['data']['cards']:
                    for card_version_source in card_source['numbers']:
                        if not sn_has_language_code(
                                card_version_source['print_tag']):
                            card_set.with_language_code = False
                            break

                    if not card_set.with_language_code:
                        break

                new_card_versions = {}

                for card_source in response.body['data']['cards']:
                    card = Card.find_or_create(
                        name=card_source['name']
                    )

                    for card_version_source in card_source['numbers']:
                        set_number = sn_normalize(
                            card_version_source['print_tag'],
                            card_set.with_language_code
                        )
                        rarity = slugify(card_version_source['rarity'])

                        if (set_number in new_card_versions and
                                rarity in new_card_versions[
                                    set_number]):
                            new_card_versions[set_number][rarity][
                                'price_data'] = (combine_prices(
                                    new_card_versions[
                                        set_number][rarity]['price_data'],
                                    card_version_source['price_data']))
                        else:
                            if set_number not in new_card_versions:
                                new_card_versions[set_number] = {}

                            new_card_versions[set_number][rarity] = {
                                'card': card
                            }

                            new_card_versions[set_number][
                                rarity]['price_data'] = (
                                    card_version_source['price_data'])

                new_card_versions_pks = []

                for set_number, rarities in new_card_versions.iteritems():
                    for rarity, data in rarities.iteritems():
                        card_version = CardVersion.find_or_create(
                            set_number=set_number,
                            card=data['card'],
                            card_set=card_set,
                            rarity=rarity
                        )

                        new_card_versions_pks.append(card_version.pk)

                        data['card_version'] = card_version

                        if (data['price_data'] and
                                data['price_data']['status'] == 'success'):
                            card_version.set_prices(data['price_data'])
                        else:
                            card_version.clear_prices()

                junk_card_versions = (
                    CardVersion.objects
                    .filter(card_set=card_set)
                    .exclude(pk__in=new_card_versions_pks)
                    .prefetch_related('user_card_versions',
                                      'user_card_versions__user')
                    .select_related('rarity')
                    .distinct())

                for card_version in junk_card_versions:
                    set_number = sn_normalize(
                        card_version.set_number,
                        card_set.with_language_code
                    )
                    rarity = unicode(card_version.rarity.identifier)

                    try:
                        actual_card_version = new_card_versions[set_number][
                            rarity]['card_version']
                    except:
                        try:
                            actual_card_version = new_card_versions[
                                set_number].itervalues().next()['card_version']
                        except:
                            card_version.dirty = True
                            card_version.save()
                            continue

                    with transaction.atomic():
                        for item in card_version.user_card_versions.all():
                            try:
                                user_card_version = (
                                    UserCardVersion.objects
                                    .get(card_version=card_version,
                                         user=item.user))
                                user_card_version.have_count += item.have_count
                                user_card_version.save()
                            except:
                                item.card_version = actual_card_version
                                item.save()
                    card_version.delete()

                card_set.requires_update = False
                card_set.save()

                output(u'Fetched.')
        else:
            step.set(0)
