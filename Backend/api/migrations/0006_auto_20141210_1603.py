# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20141208_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localizedword',
            name='name',
            field=models.TextField(),
            #preserve_default=True,
        ),
        migrations.AlterField(
            model_name='word',
            name='name',
            field=models.TextField(),
            #preserve_default=True,
        ),
    ]
