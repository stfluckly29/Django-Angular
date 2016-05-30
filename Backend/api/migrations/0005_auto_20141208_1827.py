# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20141203_1843'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='localizedword',
            unique_together=set([('app', 'word', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='word',
            unique_together=set([('app', 'name')]),
        ),
    ]
