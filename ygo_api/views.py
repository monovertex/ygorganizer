
from ygo_cards.models import (CardVersion, UserCardVersion, Card, UserCard,
                              Deck, CardSet, UserCardVersionStatistics)
from ygo_cards.serializers import (CardSerializerFull,
                                   UserCardVersionSerializer,
                                   UserCardSerializer, DeckSerializerFull)
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, filters
from rest_framework import serializers
from rest_framework_extensions.cache.mixins import CacheResponseMixin


class CardViewSet(CacheResponseMixin, viewsets.ReadOnlyModelViewSet):
    queryset = (Card.objects.all()
                .prefetch_related('card_versions', 'card_monster_types'))
    lookup_value_regex = '.+'
    serializer_class = CardSerializerFull
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'description', 'identifier', 'number',
                     'card_type__name', 'monster_attribute__name',
                     'spell_trap_property__name')
    lookup_field = 'identifier'


class UserCardView(APIView):

    def update(self, request, model):
        want_count = max(0, int(request.data.get('want_count', 0)))

        try:
            model.want_count = want_count

            model.save()

            return Response(UserCardSerializer(model).data)
        except:
            return Response(status=400)

    def put(self, request, format=None):
        model = UserCard.objects.get(id=request.data.get('id'),
                                     card_id=request.data.get('card'),
                                     user=request.user)

        return self.update(request, model)

    def post(self, request, format=None):
        model = UserCard(card_id=request.data.get('card'), user=request.user)

        return self.update(request, model)


class UserCardVersionView(APIView):

    def update(self, request, model):
        have_count = max(0, int(request.data.get('have_count', 0)))

        try:
            model.have_count = have_count

            model.save()

            return Response(UserCardVersionSerializer(model).data)
        except:
            return Response(status=400)

    def put(self, request, format=None):
        model = UserCardVersion.objects.get(
            id=request.data.get('id'),
            card_version_id=request.data.get('card_version'),
            user=request.user
        )

        return self.update(request, model)

    def post(self, request, format=None):
        model = UserCardVersion(
            card_version_id=request.data.get('card_version'),
            user=request.user
        )

        return self.update(request, model)


class DeckViewSet(viewsets.ModelViewSet):
    queryset = Deck.objects.all()
    serializer_class = DeckSerializerFull


class CardSerializerLocal(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = ('id', 'identifier', 'name', 'card_type', 'status_advanced',
                  'image_small_tag')


class CardVersionSerializerLocal(serializers.ModelSerializer):

    card = CardSerializerLocal()

    class Meta:
        model = CardVersion
        fields = ('id', 'set_number', 'rarity',
                  'price_low', 'price_avg', 'price_high', 'card', 'card_set',
                  'price_shift')


class DictObject:
    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)


class CardVersionView(APIView):

    def get_request_parameters(self, request):
        page = int(request.GET.get('page', 0))
        per_page = int(request.GET.get('per_page', 20))
        if per_page < 0:
            per_page = 20
        offset = page * per_page

        return (
            request.GET.get('sort_by', u'id').replace('.', '__'),
            request.GET.get('order') == 'desc',
            request.GET.get('q', None),
            offset,
            (offset + per_page)
        )

    def get(self, view, request, *args, **kwargs):
        (order_by, reverse, search,
            limit_start, limit_end) = self.get_request_parameters(request)

        # Build the basic queryset. We select only the values we need from
        # the query, for optimization purposes.
        queryset = (CardVersion.objects.all()
                    .select_related('card')
                    .only('id', 'set_number', 'rarity', 'card_set_id',
                          'price_low', 'price_avg', 'price_high',
                          'price_shift',

                          'card__name', 'card__card_type', 'card__id',
                          'card__status_advanced', 'card__image_small'))

        # Special cases when ordered by have count.
        if order_by == 'user_card_version__have_count':
            queryset = queryset.extra(
                select={
                    order_by: """
                        SELECT `ucv`.`have_count`
                        FROM `ygo_cards_usercardversion` `ucv`
                        WHERE
                            `ucv`.`card_version_id` =
                                `ygo_cards_cardversion`.`id`
                            AND `ucv`.`user_id` = {}
                    """.format(request.user.pk)
                },
                order_by=[order_by, 'ygo_cards_cardversion.set_number']
            )

        # Order by anything else.
        else:
            queryset = queryset.order_by(order_by, 'set_number')

        # If we have to search, filter the queryset.
        if search is not None:
            queryset = queryset.filter(search_text__icontains=search)

        # If we're in a collection, filter only the versions with a have count
        # larger than 0.
        if view == 'collection':
            queryset = queryset.extra(where=["""
                (SELECT ucv.have_count
                    FROM ygo_cards_usercardversion ucv
                    WHERE ucv.card_version_id = ygo_cards_cardversion.id
                        AND ucv.user_id = {}) > 0
            """.format(request.user.pk)])

        # If the queryset should be sorted in descendant order, reverse it.
        if reverse:
            queryset = queryset.reverse()

        # Count all the results, to provide this info in the front-end.
        count = queryset.count()

        # Limit the results.
        queryset = queryset[limit_start:limit_end]

        subtotal_count = queryset.count()

        # Serialize the results.
        data = CardVersionSerializerLocal(queryset, many=True).data

        # Grab all the have counts and append them in the result. It's the most
        # optimal method, as we only grab those UserCardVersion models we need.
        card_version_ids = [x['id'] for x in data]
        card_ids = set([x['card']['id'] for x in data])

        user_card_versions = request.user.user_card_versions.filter(
            card_version_id__in=card_version_ids)
        user_card_versions_grouped = {}
        for user_card_version in user_card_versions:
            user_card_versions_grouped[
                user_card_version.card_version_id] = user_card_version

        if view == 'collection':
            subtotal_count = 0
            subtotal_price_shift = 0
            subtotal_price_low = 0
            subtotal_price_avg = 0
            subtotal_price_high = 0

            try:
                total_statistics = UserCardVersionStatistics.objects.get(
                    pk=request.user.pk)
            except:
                total_statistics = DictObject({
                    'count': 0,
                    'price_shift': 0,
                    'price_low': 0,
                    'price_avg': 0,
                    'price_high': 0
                })

        # If needed, grab all the want counts and append them in the result.
        if view == 'browse':
            user_cards = request.user.user_cards.filter(
                card_id__in=card_ids)
            user_cards_grouped = {}
            for user_card in user_cards:
                user_cards_grouped[user_card.card_id] = user_card

        for card_version in data:
            try:
                user_card_version = user_card_versions_grouped[
                    card_version['id']]
            except:
                user_card_version = UserCardVersion(
                    card_version_id=card_version['id'],
                    user=request.user
                )

            card_version['user_card_version'] = UserCardVersionSerializer(
                user_card_version).data

            if view == 'collection':
                subtotal_count += user_card_version.have_count

                try:
                    subtotal_price_shift += (
                        user_card_version.have_count *
                        card_version['price_shift'])
                except:
                    pass

                try:
                    subtotal_price_low += (
                        user_card_version.have_count *
                        card_version['price_low'])
                except:
                    pass

                try:
                    subtotal_price_avg += (
                        user_card_version.have_count *
                        card_version['price_avg'])
                except:
                    pass

                try:
                    subtotal_price_high += (
                        user_card_version.have_count *
                        card_version['price_high'])
                except:
                    pass

            if view == 'browse':
                try:
                    user_card = user_cards_grouped[card_version['card']['id']]
                except:
                    user_card = UserCard(
                        card_id=card_version['card']['id'],
                        user=request.user
                    )

                card_version['card']['user_card'] = UserCardSerializer(
                    user_card).data

        additional_data = {
            'total_entries': count,
        }

        if view == 'collection':
            additional_data.update({
                'subtotal_count': subtotal_count,
                'subtotal_price_shift': subtotal_price_shift,
                'subtotal_price_low': subtotal_price_low,
                'subtotal_price_avg': subtotal_price_avg,
                'subtotal_price_high': subtotal_price_high,

                'total_count': total_statistics.count,
                'total_price_shift': total_statistics.price_shift,
                'total_price_low': total_statistics.price_low,
                'total_price_avg': total_statistics.price_avg,
                'total_price_high': total_statistics.price_high
            })

        return Response([additional_data, data])


class BrowseView(CardVersionView):

    def get(self, request, *args, **kwargs):
        return super(BrowseView, self).get('browse', request)


class CollectionView(CardVersionView):

    def get(self, request, *args, **kwargs):
        return super(CollectionView, self).get('collection', request)


# class WishlistView(CardVersionView):

#     def get(self, request, *args, **kwargs):
#         (order_by, reverse, query,
#             limit_start, limit_end) = self.get_request_parameters(request)

#         queryset = (request.user.user_cards.all()
#                     .prefetch_related('card__card_monster_types'))

#         if order_by == 'count':
#             queryset = queryset.extra(
#                 select={
#                     order_by: """
#                         SELECT `ucv`.`count`
#                         FROM `ygo_cards_usercardversion` `ucv`
#                         WHERE
#                             `ucv`.`card_version_id` = `ygo_cards_cardversion`.`id`
#                             AND `ucv`.`user_id` = {}
#                     """.format(request.user.id)
#                 },
#                 order_by=[order_by]
#             )
#         else:
#             queryset = queryset.order_by(order_by)

#         if reverse:
#             queryset = queryset.reverse()

#         if query is not None:
#             queryset = queryset.filter(
#                 Q(name__icontains=query)
#                 | Q(description__icontains=query)
#             )

#         count = queryset.count()

#         queryset = queryset[limit_start:limit_end]

#         data = CardSerializerFull(queryset, many=True).data

#         return Response([{'total_entries': count}, data])
