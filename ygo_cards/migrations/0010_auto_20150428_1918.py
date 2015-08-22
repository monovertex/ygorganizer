# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ygo_cards', '0009_auto_20150424_1955'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cardversion',
            unique_together=set([('set_number', 'rarity')]),
        ),
    ]
