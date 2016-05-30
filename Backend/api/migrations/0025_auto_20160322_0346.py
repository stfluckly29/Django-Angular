# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_auto_20160316_0358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='token',
            field=models.CharField(default=b'sdOF6BL56YY4RMuO', max_length=16),
        ),
        migrations.AlterField(
            model_name='usercode',
            name='code',
            field=models.CharField(default=b'zEB1i9mciDBYN4Pd', max_length=40, serialize=False, primary_key=True),
        ),
    ]
