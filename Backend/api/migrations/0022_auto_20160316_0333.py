# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_auto_20160302_0402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='token',
            field=models.CharField(default=b'GJQ6EmfjE6tO1yO1', max_length=16),
        ),
        migrations.AlterField(
            model_name='usercode',
            name='code',
            field=models.CharField(default=b'zDZ2JZ2u151NObhb', max_length=40, serialize=False, primary_key=True),
        ),
    ]
