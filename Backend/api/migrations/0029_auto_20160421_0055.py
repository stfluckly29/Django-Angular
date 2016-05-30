# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import api.models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_auto_20160419_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default=b'', null=True, upload_to=api.models.upload_to, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='app',
            name='token',
            field=models.CharField(default=b'Xb28rZ0BBjjEpsrB', max_length=16),
        ),
        migrations.AlterField(
            model_name='usercode',
            name='code',
            field=models.CharField(default=b'fkxrDDL6oMf5vnWp', max_length=40, serialize=False, primary_key=True),
        ),
    ]
