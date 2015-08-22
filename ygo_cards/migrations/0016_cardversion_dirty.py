# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ygo_cards', '0015_cardset_with_language_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardversion',
            name='dirty',
            field=models.BooleanField(default=False),
        ),
    ]
