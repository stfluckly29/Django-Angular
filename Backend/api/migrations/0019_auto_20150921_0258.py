# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_auto_20150921_0255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='usercode',
            name='code',
            field=models.CharField(default=b'3pyf0pwNmQ2bIbVW', max_length=40, serialize=False, primary_key=True),
        ),
    ]
