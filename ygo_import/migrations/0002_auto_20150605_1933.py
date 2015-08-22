# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ygo_import', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importdata',
            name='step',
            field=models.IntegerField(default=0, choices=[(0, b'Upload'), (1, b'Select Rarities'), (2, b'Confirm Import'), (3, b'Processing'), (4, b'Success')]),
        ),
    ]
