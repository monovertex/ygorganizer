# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ygo_cards', '0014_usercardversionstatistics'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardset',
            name='with_language_code',
            field=models.BooleanField(default=True),
        ),
    ]
