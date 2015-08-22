# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ygo_cards', '0005_deck_deckcard_usercard'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deck',
            name='count',
        ),
        migrations.AddField(
            model_name='deckcard',
            name='type',
            field=models.CharField(default=b'm', max_length=1, choices=[
                                   (b'm', b'Main'), (b'e', b'extra'), (b's', b'side')]),
            preserve_default=True,
        ),
    ]
