# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20150918_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='updated',
            field=models.DateField(default=datetime.date(2015, 9, 18), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='word',
            name='translated',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usercode',
            name='code',
            field=models.CharField(default=b'yFiKTkjOMJjoKwqc', max_length=40, serialize=False, primary_key=True),
        ),
    ]
