# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_auto_20160421_0055'),
    ]

    operations = [
        migrations.RenameField(
            model_name='app',
            old_name='app_link',
            new_name='app_id',
        ),
        migrations.AlterField(
            model_name='app',
            name='token',
            field=models.CharField(default=b'zMFqlc3RBn8XdkXJ', max_length=16),
        ),
        migrations.AlterField(
            model_name='usercode',
            name='code',
            field=models.CharField(default=b'Iul5mVOrfeWUl6N3', max_length=40, serialize=False, primary_key=True),
        ),
    ]
