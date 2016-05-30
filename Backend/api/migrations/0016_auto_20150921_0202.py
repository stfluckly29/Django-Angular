# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20150918_1717'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='word',
            name='translated',
        ),
        migrations.AlterField(
            model_name='usercode',
            name='code',
            field=models.CharField(default=b'9Z1u7BOfSdIcq81q', max_length=40, serialize=False, primary_key=True),
        ),
    ]
