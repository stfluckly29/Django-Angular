# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_usercode'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=255)),
                ('bundle_identifier', models.CharField(default=b'', max_length=255)),
                ('cert_type', models.BooleanField(default=False)),
                ('exp_date', models.DateTimeField()),
                ('file_name', models.CharField(max_length=255)),
                ('app', models.ForeignKey(related_name=b'certs', to='api.App')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='usercode',
            name='code',
            field=models.CharField(default=b'ma3VICraiok3Hk8N', max_length=40, serialize=False, primary_key=True),
        ),
    ]
