from __future__ import absolute_import

from celery import shared_task
from .models import ImportData
from .forms import UploadForm
from django.contrib.auth.models import User
from ygo_cards.models import UserCardVersion
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def process_import(user_id):
    try:
        user = User.objects.select_related('import_data').get(pk=user_id)
        import_data = user.import_data

        data = import_data.get_data()

        current_card_versions = {}

        if data['mode'] == UploadForm.MODE_REPLACE:
            user.user_card_versions.all().delete()
        else:
            user_card_versions = (user.user_card_versions
                                  .select_related('card_version')
                                  .all())

            for user_card_version in user_card_versions:
                current_card_versions[user_card_version.card_version.pk] = (
                    user_card_version)

        for set_number, rarities in data['all_valid_set_numbers'].iteritems():
            for rarity_pk, info in rarities.iteritems():
                if info['pk'] in current_card_versions:
                    user_card_version = current_card_versions[info['pk']]
                else:
                    user_card_version = UserCardVersion(
                        user=user, card_version_id=info['pk'])

                user_card_version.have_count = (
                    user_card_version.have_count + info['count'])

                user_card_version.save()

        import_data.step = ImportData.STEP_SUCCESS
        import_data.save()
    except:
        logger.exception('Task Error')
