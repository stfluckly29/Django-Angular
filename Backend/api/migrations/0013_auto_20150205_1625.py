# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20150205_1452'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificate',
            name='exp_date',
        ),
        migrations.AddField(
            model_name='certificate',
            name='expiry_date',
            field=models.CharField(default=b'', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usercode',
            name='code',
            field=models.CharField(default=b'sQvqT6LUaPSpVXWu', max_length=40, serialize=False, primary_key=True),
        ),
    ]
