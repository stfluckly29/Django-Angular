# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_auto_20160406_0240'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='app_link',
            field=models.CharField(default=b'', max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='app',
            name='logo',
            field=models.CharField(default=b'', max_length=512, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='app',
            name='screenshot',
            field=models.CharField(default=b'', max_length=512, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='app',
            name='token',
            field=models.CharField(default=b'xMOlTGiLzBPG60Cf', max_length=16),
        ),
        migrations.AlterField(
            model_name='usercode',
            name='code',
            field=models.CharField(default=b'B25WJn6456mkWe1s', max_length=40, serialize=False, primary_key=True),
        ),
    ]
