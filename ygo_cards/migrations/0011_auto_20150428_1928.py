# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ygo_cards', '0010_auto_20150428_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardversion',
            name='set_number',
            field=models.CharField(max_length=15),
        ),
    ]
