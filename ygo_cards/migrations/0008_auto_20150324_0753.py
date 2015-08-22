# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ygo_cards', '0007_remove_deckcard_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usercard',
            old_name='count',
            new_name='want_count',
        ),
        migrations.RenameField(
            model_name='usercardversion',
            old_name='count',
            new_name='have_count',
        ),
        migrations.AlterUniqueTogether(
            name='cardmonstertype',
            unique_together=set([('card', 'monster_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='usercard',
            unique_together=set([('user', 'card')]),
        ),
    ]
