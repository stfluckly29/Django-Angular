# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20150921_0207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='updated',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='usercode',
            name='code',
            field=models.CharField(default=b'BPW5kmvXj8t2RIQw', max_length=40, serialize=False, primary_key=True),
        ),
    ]
