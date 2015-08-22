# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('ygo_cards', '0013_auto_20150428_2041'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCardVersionStatistics',
            fields=[
                ('user', models.ForeignKey(related_name='statistics', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('count', models.PositiveIntegerField(default=0)),
                ('price_low', models.FloatField(null=True, blank=True)),
                ('price_avg', models.FloatField(null=True, blank=True)),
                ('price_high', models.FloatField(null=True, blank=True)),
                ('price_shift', models.FloatField(null=True, blank=True)),
            ],
            options={
                'managed': False,
            },
        ),
    ]
