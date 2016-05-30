# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20141210_1612'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCode',
            fields=[
                ('code', models.CharField(default=b'w3cydu6440X9fTxo', max_length=40, serialize=False, primary_key=True)),
                ('is_signup', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
