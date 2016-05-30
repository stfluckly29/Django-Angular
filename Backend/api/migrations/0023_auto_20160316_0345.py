# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_auto_20160316_0333'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppFeedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lang', models.CharField(max_length=7, choices=[(b'ar', b'Arabic'), (b'ca', b'Catalan'), (b'zh-Hans', b'Chinese(Simplified)'), (b'zh-Hant', b'Chinese(Traditional)'), (b'hr', b'Croatian'), (b'cs', b'Czech'), (b'nl', b'Dutch'), (b'da', b'Danish'), (b'en', b'English'), (b'en-GB', b'English (British)'), (b'en-AU', b'English (Australian)'), (b'fi', b'Finnish'), (b'fr', b'French'), (b'de', b'German'), (b'el', b'Greek'), (b'he', b'Hebrew'), (b'hu', b'Hungarian'), (b'id', b'Indonesian'), (b'it', b'Italian'), (b'ja', b'Japanese'), (b'ko', b'Korean'), (b'es-MX', b'Mexican Spanish'), (b'ms', b'Malay'), (b'nb', b'Norwegian (Bokmal)'), (b'pl', b'Polish'), (b'pt', b'Portuguese'), (b'pt-PT', b'Portuguese (Portugal)'), (b'ro', b'Romanian'), (b'ru', b'Russian'), (b'sk', b'Slovak'), (b'es', b'Spanish'), (b'sv', b'Swedish'), (b'th', b'Thai'), (b'tr', b'Turkish'), (b'uk', b'Ukrainian'), (b'vi', b'Vietnamese')])),
                ('satisfied', models.IntegerField(default=0)),
                ('unsatisfied', models.IntegerField(default=0)),
                ('app', models.ForeignKey(related_name=b'app_feedback', to='api.App')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LocalizedWordFeedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lang', models.CharField(max_length=7, choices=[(b'ar', b'Arabic'), (b'ca', b'Catalan'), (b'zh-Hans', b'Chinese(Simplified)'), (b'zh-Hant', b'Chinese(Traditional)'), (b'hr', b'Croatian'), (b'cs', b'Czech'), (b'nl', b'Dutch'), (b'da', b'Danish'), (b'en', b'English'), (b'en-GB', b'English (British)'), (b'en-AU', b'English (Australian)'), (b'fi', b'Finnish'), (b'fr', b'French'), (b'de', b'German'), (b'el', b'Greek'), (b'he', b'Hebrew'), (b'hu', b'Hungarian'), (b'id', b'Indonesian'), (b'it', b'Italian'), (b'ja', b'Japanese'), (b'ko', b'Korean'), (b'es-MX', b'Mexican Spanish'), (b'ms', b'Malay'), (b'nb', b'Norwegian (Bokmal)'), (b'pl', b'Polish'), (b'pt', b'Portuguese'), (b'pt-PT', b'Portuguese (Portugal)'), (b'ro', b'Romanian'), (b'ru', b'Russian'), (b'sk', b'Slovak'), (b'es', b'Spanish'), (b'sv', b'Swedish'), (b'th', b'Thai'), (b'tr', b'Turkish'), (b'uk', b'Ukrainian'), (b'vi', b'Vietnamese')])),
                ('satisfied', models.IntegerField(default=0)),
                ('unsatisfied', models.IntegerField(default=0)),
                ('app', models.ForeignKey(related_name=b'lw_feedback', to='api.App')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='app',
            name='token',
            field=models.CharField(default=b'ocEnuvnqGbVYtJ1S', max_length=16),
        ),
        migrations.AlterField(
            model_name='usercode',
            name='code',
            field=models.CharField(default=b'E0l9IZyVqjAwzSR1', max_length=40, serialize=False, primary_key=True),
        ),
    ]
