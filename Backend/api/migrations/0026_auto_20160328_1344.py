# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_auto_20160322_0346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='token',
            field=models.CharField(default=b'f9jpXb5XSvFHDiD6', max_length=16),
        ),
        migrations.AlterField(
            model_name='appfeedback',
            name='satisfied',
            field=models.IntegerField(default=0, blank=True),
        ),
        migrations.AlterField(
            model_name='appfeedback',
            name='unsatisfied',
            field=models.IntegerField(default=0, blank=True),
        ),
        migrations.AlterField(
            model_name='localizedwordfeedback',
            name='satisfied',
            field=models.IntegerField(default=0, blank=True),
        ),
        migrations.AlterField(
            model_name='localizedwordfeedback',
            name='unsatisfied',
            field=models.IntegerField(default=0, blank=True),
        ),
        migrations.AlterField(
            model_name='usercode',
            name='code',
            field=models.CharField(default=b'0XjNHI1b4SHZKhbu', max_length=40, serialize=False, primary_key=True),
        ),
    ]
