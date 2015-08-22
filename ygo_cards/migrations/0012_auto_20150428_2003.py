# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ygo_cards', '0011_auto_20150428_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardversion',
            name='price_shift',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='cardversion',
            name='price_shift_180',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='cardversion',
            name='price_shift_21',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='cardversion',
            name='price_shift_3',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='cardversion',
            name='price_shift_30',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='cardversion',
            name='price_shift_365',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='cardversion',
            name='price_shift_7',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='cardversion',
            name='price_shift_90',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
