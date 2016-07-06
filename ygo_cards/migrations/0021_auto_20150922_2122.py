# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ygo_cards', '0020_cardset_session_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cardset',
            old_name='session_id',
            new_name='cookie',
        ),
    ]
