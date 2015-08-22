# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import easy_thumbnails.fields
import ygo_cards.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(unique=True, max_length=255)),
                ('number', models.CharField(
                    max_length=8, null=True, blank=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(
                    max_length=255, null=True, blank=True)),
                ('requires_update', models.BooleanField(default=True)),
                ('monster_level', models.IntegerField(null=True, blank=True)),
                ('monster_attack', models.CharField(
                    max_length=10, null=True, blank=True)),
                ('monster_defense', models.CharField(
                    max_length=10, null=True, blank=True)),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(
                    null=True, upload_to=ygo_cards.models.card_image_full, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CardMonsterType',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('card', models.ForeignKey(
                    related_name=b'card_monster_types', to='ygo_cards.Card')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CardSet',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(unique=True, max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('requires_update', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CardStatus',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CardType',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CardVersion',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('set_number', models.CharField(unique=True, max_length=15)),
                ('price_low', models.FloatField(null=True, blank=True)),
                ('price_avg', models.FloatField(null=True, blank=True)),
                ('price_high', models.FloatField(null=True, blank=True)),
                ('card', models.ForeignKey(
                    related_name=b'card_versions', to='ygo_cards.Card')),
                ('card_set', models.ForeignKey(
                    related_name=b'card_versions', to='ygo_cards.CardSet')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MonsterAttribute',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MonsterType',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rarity',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SpellTrapProperty',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserCardVersion',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('want_count', models.PositiveIntegerField(default=0)),
                ('have_count', models.PositiveIntegerField(default=0)),
                ('card_version', models.ForeignKey(
                    related_name=b'user_card_versions', to='ygo_cards.CardVersion')),
                ('user', models.ForeignKey(
                    related_name=b'user_card_versions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='usercardversion',
            unique_together=set([('user', 'card_version')]),
        ),
        migrations.AddField(
            model_name='cardversion',
            name='rarity',
            field=models.ForeignKey(
                related_name=b'card_versions', to='ygo_cards.Rarity'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cardmonstertype',
            name='monster_type',
            field=models.ForeignKey(
                related_name=b'card_monster_types', to='ygo_cards.MonsterType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='card_type',
            field=models.ForeignKey(
                related_name=b'cards', blank=True, to='ygo_cards.CardType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='monster_attribute',
            field=models.ForeignKey(
                related_name=b'cards', blank=True, to='ygo_cards.MonsterAttribute', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='spell_trap_property',
            field=models.ForeignKey(
                related_name=b'cards', blank=True, to='ygo_cards.SpellTrapProperty', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='status_advanced',
            field=models.ForeignKey(
                related_name=b'advanced_cards', blank=True, to='ygo_cards.CardStatus', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='status_traditional',
            field=models.ForeignKey(
                related_name=b'traditional_cards', blank=True, to='ygo_cards.CardStatus', null=True),
            preserve_default=True,
        ),
    ]
