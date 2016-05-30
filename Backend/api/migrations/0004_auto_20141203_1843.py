# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_app_enabled'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wordcms',
            name='localized_word',
        ),
        migrations.RemoveField(
            model_name='wordcms',
            name='word',
        ),
        migrations.DeleteModel(
            name='WordCMS',
        ),
        migrations.AddField(
            model_name='localizedword',
            name='selected',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
