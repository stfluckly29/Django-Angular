# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20150205_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='exp_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='usercode',
            name='code',
            field=models.CharField(default=b'SMModE135qsklHG4', max_length=40, serialize=False, primary_key=True),
        ),
    ]
