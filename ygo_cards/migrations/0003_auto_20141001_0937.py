# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ygo_cards', '0002_remove_cardset_identifier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardset',
            name='name',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
