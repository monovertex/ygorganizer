# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ygo_cards', '0017_remove_cardversion_dirty'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardset',
            name='dirty',
            field=models.BooleanField(default=False),
        ),
    ]
