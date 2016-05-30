# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email_verified', models.BooleanField(default=False)),
                ('company', models.CharField(default=b'', max_length=255, blank=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('owner', models.ForeignKey(related_name='apps', default=None, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LocalizedWord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('lang', models.CharField(max_length=7, choices=[(b'ar', b'Arabic'), (b'ca', b'Catalan'), (b'zh-Hans', b'Chinese(Simplified)'), (b'zh-Hant', b'Chinese(Traditional)'), (b'hr', b'Croatian'), (b'cs', b'Czech'), (b'nl', b'Dutch'), (b'da', b'Danish'), (b'en', b'English'), (b'en-GB', b'English (British)'), (b'en-AU', b'English (Australian)'), (b'fi', b'Finnish'), (b'fr', b'French'), (b'de', b'German'), (b'el', b'Greek'), (b'he', b'Hebrew'), (b'hu', b'Hungarian'), (b'id', b'Indonesian'), (b'it', b'Italian'), (b'ja', b'Japanese'), (b'ko', b'Korean'), (b'es-MX', b'Mexican Spanish'), (b'ms', b'Malay'), (b'nb', b'Norwegian (Bokmal)'), (b'pl', b'Polish'), (b'pt', b'Portuguese'), (b'pt-PT', b'Portuguese (Portugal)'), (b'ro', b'Romanian'), (b'ru', b'Russian'), (b'sk', b'Slovak'), (b'es', b'Spanish'), (b'sv', b'Swedish'), (b'th', b'Thai'), (b'tr', b'Turkish'), (b'uk', b'Ukrainian'), (b'vi', b'Vietnamese')])),
                ('app', models.ForeignKey(to='api.App')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('app', models.ForeignKey(related_name='words', to='api.App')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WordCMS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('localized_word', models.ForeignKey(related_name='local_words', to='api.LocalizedWord')),
                ('word', models.ForeignKey(to='api.Word')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='localizedword',
            name='word',
            field=models.ForeignKey(to='api.Word'),
            preserve_default=True,
        ),
    ]
