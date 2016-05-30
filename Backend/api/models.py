from django.db import models
from django.contrib.auth.models import AbstractUser
import random
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save, post_init, post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models import Q
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.contrib.sites.models import Site
from django.conf import settings
import uuid
import os

def random_key():
    return ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxzyABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(16))

LANG_CHOICES = (
    ('ar', 'Arabic'),
    ('ca', 'Catalan'),
    ('zh-Hans', 'Chinese(Simplified)'),
    ('zh-Hant', 'Chinese(Traditional)'),
    ('hr', 'Croatian'),
    ('cs', 'Czech'),
    ('nl', 'Dutch'),
    ('da', 'Danish'),
    ('en', 'English'),
    ('en-GB', 'English (British)'),
    ('en-AU', 'English (Australian)'),
    ('fi', 'Finnish'),
    ('fr', 'French'),
    ('de', 'German'),
    ('el', 'Greek'),
    ('he', 'Hebrew'),
    ('hu', 'Hungarian'),
    ('id', 'Indonesian'),
    ('it', 'Italian'),
    ('ja', 'Japanese'),
    ('ko', 'Korean'),
    ('es-MX', 'Mexican Spanish'),
    ('ms', 'Malay'),
    ('nb', 'Norwegian (Bokmal)'),
    ('pl', 'Polish'),
    ('pt', 'Portuguese'),
    ('pt-PT', 'Portuguese (Portugal)'),
    ('ro', 'Romanian'),
    ('ru', 'Russian'),
    ('sk', 'Slovak'),
    ('es', 'Spanish'),
    ('sv', 'Swedish'),
    ('th', 'Thai'),
    ('tr', 'Turkish'),
    ('uk', 'Ukrainian'),
    ('vi', 'Vietnamese'),
)


def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    full_path = 'avatars/{}/{}'.format(instance.id, filename)

    return full_path


class User(AbstractUser):
    email_verified = models.BooleanField(default=False)
    company = models.CharField(max_length=255, blank=True, default='')
    avatar = models.ImageField(blank=True, null=True, upload_to=upload_to, editable=True, default='')


class UserCode(models.Model):
    user = models.ForeignKey(User)
    code = models.CharField(max_length=40, primary_key=True, default=random_key())
    is_signup = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code


class App(models.Model):
    name = models.CharField(max_length=255, blank=False)
    owner = models.ForeignKey(User, related_name='apps')
    enabled = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True, blank=False)
    app_id = models.CharField(max_length=255, blank=True, default='')
    logo = models.CharField(max_length=512, blank=True, default='')
    screenshot = models.CharField(max_length=512, blank=True, default='')
    token = models.CharField(max_length=16, blank=False, default=random_key())


class Certificate(models.Model):
    app = models.ForeignKey(App, blank=False, related_name='certs')
    name = models.CharField(max_length=255, default='')
    bundle_identifier = models.CharField(max_length=255, default='')
    cert_type = models.BooleanField(default=False)
    expiry_date = models.CharField(max_length=255, default='')
    file_name = models.CharField(max_length=255)


class Word(models.Model):
    app = models.ForeignKey(App, blank=False, related_name='words')
    name = models.TextField(blank=False)

    class Meta:
        unique_together = ("app", "name")


class LocalizedWord(models.Model):
    name = models.TextField(blank=True)
    lang = models.CharField(max_length=7, choices=LANG_CHOICES)
    word = models.ForeignKey(Word, blank=False)
    app = models.ForeignKey(App,  blank=False)
    selected = models.BooleanField(default=True)

    class Meta:
        unique_together = ("app", "word", "lang")


class AppFeedback(models.Model):
    app = models.ForeignKey(App, blank=False, related_name='app_feedback')
    lang = models.CharField(max_length=7, choices=LANG_CHOICES)
    satisfied = models.IntegerField(blank=True, default=0)
    unsatisfied = models.IntegerField(blank=True, default=0)


class DailyAppStats(models.Model):
    app = models.ForeignKey(App, blank=False, related_name='daily_app_stats')
    hit_count = models.IntegerField(blank=False, default=0)
    reg_date = models.CharField(max_length=10, blank=True)
    lang = models.CharField(max_length=7, choices=LANG_CHOICES)


class MonthlyAppStats(models.Model):
    app = models.ForeignKey(App, blank=False, related_name='monthly_app_stats')
    hit_count = models.IntegerField(blank=False, default=0)
    reg_month = models.CharField(max_length=7, blank=True)
    lang = models.CharField(max_length=7, choices=LANG_CHOICES)


class LocalizedWordFeedback(models.Model):
    app = models.ForeignKey(App, blank=False, related_name='lw_feedback')
    word = models.ForeignKey(Word, blank=False)
    lang = models.CharField(max_length=7, choices=LANG_CHOICES)
    satisfied = models.IntegerField(blank=True, default=0)
    unsatisfied = models.IntegerField(blank=True, default=0)


class DeviceToken(models.Model):
    token = models.CharField(max_length=255, default='')
    app = models.ForeignKey(App, blank=False)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        token = Token.objects.create(user=instance)
        user_code, created = UserCode.objects.get_or_create(user=instance, is_signup=True)
        #current_site = Site.objects.get_current()
        reg_url = settings.DOMAIN + 'api/registration/' + user_code.code + '/'
        plaintext = get_template('email.txt')
        htmly = get_template('email.html')
        d = Context({'user': instance, 'url': reg_url})

        subject, from_email, to = 'Signup [InAppTranslation]', 'info@inapptranslation.com', instance.username
        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


def update_app(instance):
    if instance and instance.app:
        instance.app.save()

@receiver(post_save, sender=LocalizedWord)
def post_save_localized(sender, instance=None, **kwargs):
    update_app(instance)

@receiver(post_delete, sender=LocalizedWord)
def post_init_localized(sender, instance=None, **kwargs):
    update_app(instance)

@receiver(post_save, sender=Word)
def post_save_word(sender, instance=None, **kwargs):
    update_app(instance)

@receiver(post_delete, sender=Word)
def post_delete_word(sender, instance=None, **kwargs):
    update_app(instance)

@receiver(post_save, sender=App)
def post_save_app(sender, instance, created, *args, **kwargs):
    if created:
        instance.token = random_key()
        instance.save()