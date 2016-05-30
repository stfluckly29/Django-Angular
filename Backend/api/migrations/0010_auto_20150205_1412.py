# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20150205_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='exp_date',
            field=models.DateTimeField(default=None),
        ),
        migrations.AlterField(
            model_name='usercode',
            name='code',
            field=models.CharField(default=b'Ft1yXKnjN01phmeR', max_length=40, serialize=False, primary_key=True),
        ),
    ]
