# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ygo_cards', '0006_auto_20150125_2329'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deckcard',
            name='count',
        ),
    ]
