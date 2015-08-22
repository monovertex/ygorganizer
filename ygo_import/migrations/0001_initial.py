# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportData',
            fields=[
                ('user', models.OneToOneField(related_name='import_data', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('data', models.TextField(blank=True)),
                ('step', models.IntegerField(default=0, choices=[(0, b'Upload'), (1, b'Clarify Rarities'), (2, b'Confirm Import'), (3, b'Processing'), (4, b'Success')])),
            ],
        ),
    ]
