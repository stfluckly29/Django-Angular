# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_auto_20150921_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='token',
            field=models.CharField(default=b'ORYWIMPaUUUYmzNn', max_length=16),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usercode',
            name='code',
            field=models.CharField(default=b'qDanx4vh9zw9GXFb', max_length=40, serialize=False, primary_key=True),
        ),
    ]
