# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_auto_20150921_0258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localizedword',
            name='name',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='usercode',
            name='code',
            field=models.CharField(default=b'dBc4yngqmxlGnSZa', max_length=40, serialize=False, primary_key=True),
        ),
    ]
