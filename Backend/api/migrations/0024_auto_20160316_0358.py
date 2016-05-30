# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_auto_20160316_0345'),
    ]

    operations = [
        migrations.AddField(
            model_name='localizedwordfeedback',
            name='word',
            field=models.ForeignKey(default=0, to='api.Word'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='app',
            name='token',
            field=models.CharField(default=b'vpGYuR3Zv5SyEBKD', max_length=16),
        ),
        migrations.AlterField(
            model_name='usercode',
            name='code',
            field=models.CharField(default=b'bbI2hsq86I8ELOLT', max_length=40, serialize=False, primary_key=True),
        ),
    ]
