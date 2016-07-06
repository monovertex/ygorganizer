# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ygo_cards', '0016_cardversion_dirty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cardversion',
            name='dirty',
        ),
    ]
