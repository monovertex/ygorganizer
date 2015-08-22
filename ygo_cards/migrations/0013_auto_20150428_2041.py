# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ygo_cards.models
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ygo_cards', '0012_auto_20150428_2003'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='image_medium',
            field=easy_thumbnails.fields.ThumbnailerImageField(null=True, upload_to=ygo_cards.models.card_image_medium, blank=True),
        ),
        migrations.AddField(
            model_name='card',
            name='image_small',
            field=easy_thumbnails.fields.ThumbnailerImageField(null=True, upload_to=ygo_cards.models.card_image_small, blank=True),
        ),
    ]
