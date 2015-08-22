# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def update_data(apps, schema_editor):
    Card = apps.get_model('ygo_cards', 'Card')
    CardVersion = apps.get_model('ygo_cards', 'CardVersion')

    for card in Card.objects.all():
        card.search_text = ' '.join([card.identifier, card.number, card.name,
                                    card.description])
        card.save()

    for card_version in CardVersion.objects.all():
        card_version.search_text = ' '.join([
            card_version.set_number, card_version.card_set.name,
            card_version.card.search_text])

        card_version.save()


class Migration(migrations.Migration):

    dependencies = [
        ('ygo_cards', '0008_auto_20150324_0753'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='search_text',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cardversion',
            name='search_text',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.RunPython(update_data),
    ]
