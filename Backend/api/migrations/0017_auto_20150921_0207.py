# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20150921_0202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercode',
            name='code',
            field=models.CharField(default=b'50eqByPHmlcTei0E', max_length=40, serialize=False, primary_key=True),
        ),
        migrations.AlterUniqueTogether(
            name='localizedword',
            unique_together=set([('app', 'word', 'lang')]),
        ),
    ]
