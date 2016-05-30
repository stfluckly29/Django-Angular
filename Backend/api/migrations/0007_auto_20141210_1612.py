# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20141210_1603'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='localizedword',
            unique_together=set([('app', 'word', 'name', 'lang')]),
        ),
    ]
