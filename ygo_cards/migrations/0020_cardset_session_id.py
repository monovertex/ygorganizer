# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ygo_cards', '0019_cardset_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardset',
            name='session_id',
            field=models.TextField(null=True, blank=True),
        ),
    ]
