# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20141128_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='enabled',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
