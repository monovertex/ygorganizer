# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ygo_cards', '0003_auto_20141001_0937'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usercardversion',
            old_name='have_count',
            new_name='count',
        ),
        migrations.RemoveField(
            model_name='usercardversion',
            name='want_count',
        ),
    ]
