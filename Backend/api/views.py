from rest_framework import status
from .serializers import *
from .models import *
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route, action
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context
from django.core.mail.message import EmailMultiAlternatives
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.conf import settings
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from rest_framework.decorators import api_view
from OpenSSL import crypto
from datetime import datetime, timedelta, time
from rq import Queue
from redis import Redis
from util import send_push_notification
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
import pytz
import logging
import redis
from rest_framework import generics
import requests
import json
from PIL import Image

# logging.basicConfig(filename='inapp.log', level=logging.DEBUG)

def _get_random_name():
    return ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxzyABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(32))


def _local_word(app, page_size=20, _page=1, q=''):

    words = Word.objects.filter(app=app).order_by('pk')
    if q:
        words = words.filter(name__icontains=q)
    paginator = Paginator(words, page_size)
    try:
        words = paginator.page(_page)
    except PageNotAnInteger:
        _page = 1
        words = paginator.page(_page)
    except EmptyPage:
        _page = paginator.num_pages
        words = paginator.page(_page)

    translations = {}
    langs = []
    localwords = LocalizedWord.objects.filter(app=app, word__in=words).order_by('id')
    for lword in localwords:
        key = lword.word_id
        if lword.lang not in langs:
            langs.append(lword.lang)
        if not translations.get(key, False):
            translations[key] = {}

        translations[key][lword.lang] = LocalizedWordSerializer(lword).data

    word_serializer = WordSerializer(words, many=True)
    # page = paginator.page()
    return Response({'langs': langs, 'words': word_serializer.data, 'translations': translations,
                     'total_count': paginator.count, 'start_index': words.start_index(),
                     'end_index': words.end_index(), 'has_previous': words.has_previous(), 'page_size': paginator._get_num_pages(),
                     'has_next': words.has_next(), 'page_size': int(page_size or 20), 'page': _page})


class ModifiedObtainAuthToken(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.object['user'])
            if not serializer.object['user'].email_verified:
                return Response({'errors': 'Your email is not verified yet.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'token': token.key})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

modified_obtain_auth_token = ModifiedObtainAuthToken.as_view()


class CurrentUserUpdateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        u = request.user
        if 'avatar' in request.FILES:
            if u.avatar:
                u.avatar.delete()
            upload = request.FILES['avatar']
            u.avatar.save(upload.name, upload)

            image = Image.open(upload)
            (width, height) = image.size
            if width > 160 and height > 160:
                size = (160, 160)
                image = image.resize(size, Image.ANTIALIAS)

                image.save(u.avatar.path)

        for k in request.DATA:
            if k:
                if k == 'password':
                    u.set_password(request.DATA[k])
                else:
                    setattr(u, k, request.DATA[k])
        u.save()

        return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    model = User
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


    @list_route(methods=['get'])
    def stats(self, request, pk=None):
        if not request.user.is_superuser:
            return Response({'msg': "You don't have permission to see this data." }, status=status.HTTP_400_BAD_REQUEST)

        res = {}
        res['total_signup'] = User.objects.count()
        res['total_word'] = Word.objects.count()

        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        today_start = datetime.combine(today, time())
        today_end = datetime.combine(tomorrow, time())

        res['today_signup'] = User.objects.filter(date_joined__gte=today_start, date_joined__lte=today_end).count()
        # res['today_login'] = User.objects.filter(last_login__gte=today_start, last_login__lte=today_end).count()
        today = datetime.now().strftime('%Y-%m-%d')

        r = redis.StrictRedis()
        api_access = {}
        _total = 0
        for k in r.keys('%s::*' % today):
            _url = k[12:]
            _val = r.get(k)
            if "POST /api/api-token-auth" in _url:
                 _total += int(_val)
            else:
                api_access[_url] = _val

        res['api_access'] = api_access
        res['today_login'] = _total
        
        return Response([res])

    @list_route(methods=['get', 'post'])
    def forget_password(self, request):
        email = request.DATA.get('email', False)

        # validate posted params
        errors = {}
        if not email:
            errors['email'] = 'Required'

        pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(pattern, email):
            errors['email'] = 'Please input valid email address.'

        if not errors:
            user = User.objects.filter(username=email).first()
            if user:
                user_code, created = UserCode.objects.get_or_create(user=user, code=random_key(), is_signup=False)
                reg_url = settings.DOMAIN + 'api/password_reset/' + user_code.code + '/'
                plaintext = get_template('pw_reset.txt')
                htmly = get_template('pw_reset.html')
                d = Context({'url': reg_url})

                subject, from_email, to = 'Password Reset [InAppTranslation]', 'info@inapptranslation.com', user.username
                text_content = plaintext.render(d)
                html_content = htmly.render(d)
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                return Response({'status': 'success'})
            else:
                errors['email'] = "We can't find any user with the email."

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class AppViewSet(viewsets.ModelViewSet):
    serializer_class = AppSerializer
    model = App
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        app_name = self.request.QUERY_PARAMS.get('app_name')
        apps = App.objects.filter(owner=self.request.user)
        if app_name:
            apps = apps.filter(name__icontains=app_name)

        return apps

    def pre_save(self, obj):
        obj.owner = self.request.user

    @detail_route(methods=['get'])
    def words(self, request, pk=None):
        app = self.get_object()
        words = Word.objects.filter(app=app)
        serializer = WordSerializer(words, many=True)

        return Response(serializer.data)

    @detail_route(methods=['get'])
    def localwords(self, request, pk=None):
        app = self.get_object()
        page = request.QUERY_PARAMS.get('p', 1)
        page_size = request.QUERY_PARAMS.get('pz', 20)
        q = request.QUERY_PARAMS.get('q', '')
        return _local_word(app, page_size, page, q)

    @detail_route(methods=['get'])
    def web_translations(self, request, pk=None):
        app = self.get_object()
        code = request.QUERY_PARAMS.get('lang', False)
        if code and code not in [lang[0] for lang in LANG_CHOICES]:
            return Response({'errors': 'lang code is not valid.'}, status=status.HTTP_400_BAD_REQUEST)

        _filter = {'word__app': app}
        if code:
            _filter['lang'] = code

        local_words = LocalizedWord.objects.filter(**_filter).order_by('word__id')

        res = {}
        for t in local_words:
            lang = t.lang
            if not res.get(lang, False):
                res[lang] = []
            res[lang].append({'word': t.word.name, 'translation': t.name})

        return Response({'translations': [{'lang': lang, 'content': res[lang]} for lang in res]})

    @detail_route(methods=['get'])
    def translations(self, request, pk=None):

        app = self.get_object()
        last_fetch_datetime = request.META.get('HTTP_LAST_FETCH_DATETIME')
        # logging.debug(request.META)
        if last_fetch_datetime:
            last_fetch_datetime = datetime.strptime(last_fetch_datetime, '%Y-%m-%d %H:%M:%S')
            last_fetch_datetime = last_fetch_datetime.replace(tzinfo=pytz.UTC)
            if last_fetch_datetime >= app.updated:
                return Response({'updated': False, 'translations': []})

        code = request.QUERY_PARAMS.get('lang', False)
        if code and code not in [lang[0] for lang in LANG_CHOICES]:
            return Response({'errors': 'lang code is not valid.'}, status=status.HTTP_400_BAD_REQUEST)

        _filter = {'word__app': app}
        if code:
            _filter['lang'] = code

        local_words = LocalizedWord.objects.filter(**_filter)

        res = {}
        for t in local_words:
            lang = t.lang
            if not res.get(lang, False):
                res[lang] = {}
            res[lang][t.word.name] = t.name

        return Response({'updated': True, 'translations': [{'lang': lang, 'content': res[lang]} for lang in res]})

    @detail_route(methods=['delete'])
    def lang(self, request, pk=None):
        code = request.QUERY_PARAMS.get('code', False)
        if not code:
            return Response({'errors': 'lang code is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if code not in [lang[0] for lang in LANG_CHOICES]:
            return Response({'errors': 'lang code is not valid.'}, status=status.HTTP_400_BAD_REQUEST)

        LocalizedWord.objects.filter(lang=code).delete()

        return Response({'status': 'deleted'})

    @detail_route(methods=['post'])
    def add_token(self, request, pk=None):
        app = self.get_object()
        if self.request.user != app.owner:
            return Response({'errors': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        token = request.DATA.get('token')

        if not token:
            return Response({'errors': 'Token is required.'}, status=status.HTTP_400_BAD_REQUEST)

        device_token, created = DeviceToken.objects.get_or_create(token=token, app=app)

        if created:
            return Response({'status': 'inserted'})
        else:
            return Response({'status': 'already existed'})

    @detail_route(methods=['get'])
    def send_push(self, request, pk=None):
        app = self.get_object()
        if self.request.user != app.owner:
            return Response({'errors': 'Not authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        cert_type = request.QUERY_PARAMS.get('type')
        cert = Certificate.objects.filter(app=app, cert_type=(cert_type == 'prod')).first()

        if not cert:
            return Response({'errors': 'Certificate is not existed.'}, status=status.HTTP_400_BAD_REQUEST)

        path_cert = os.path.join(settings.BASE_DIR, 'certs/', cert.file_name+'_cert.pem')
        path_key = os.path.join(settings.BASE_DIR, 'certs/', cert.file_name+'_key.pem')

        redis_conn = Redis()
        q = Queue(connection=redis_conn)

        tokens = DeviceToken.objects.filter(app=app)
        for token in tokens:
            job = q.enqueue(send_push_notification, token.token, path_cert, path_key, cert_type == 'dev')

        return Response({'status': 'success'})

    @detail_route(methods=['post'])
    def add_cert(self, request, pk=None):
        app = self.get_object()
        cert_file = request.FILES.get('cert_file', False)
        cert_type = request.DATA.get('cert_type', False)
        pwd = request.DATA.get('password', '')
        file_name = _get_random_name()
        if not cert_file:
            return Response({'errors': 'certificate file should be provided.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            temp_str = cert_file.read()
            p12 = crypto.load_pkcs12(temp_str, pwd)
            cert_str = crypto.dump_certificate(crypto.FILETYPE_PEM, p12.get_certificate())
            key_str = crypto.dump_privatekey(crypto.FILETYPE_PEM, p12.get_privatekey())
            cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_str)
            details = {}
            for key, val in cert.get_subject().get_components():
                details[key] = val
            bundle_name = details['UID']
            expiry_date = datetime.strptime(cert.get_notAfter(), '%Y%m%d%H%M%Sz')
            expiry_date = expiry_date.strftime('%b %d %H:%M:%S %Y GMT')
        except Exception as e:
            print str(e)
            return Response({"errors": 'Certificate is invalid. Double check that you input correct password.'},
                            status=status.HTTP_400_BAD_REQUEST)
        if cert_type == 'product':
            if Certificate.objects.filter(app=app, cert_type=True).count() > 0:
                return Response({'errors': 'Product certification file is already exist.'},
                                status=status.HTTP_400_BAD_REQUEST)
            if 'Production' not in details['CN']:
                return Response({'errors': 'This is not production certificate.'}, status=status.HTTP_400_BAD_REQUEST)
        elif cert_type == 'develop':
            if Certificate.objects.filter(app=app, cert_type=False).count() > 0:
                return Response({'errors': 'Development certification file is already existed.'},
                                status=status.HTTP_400_BAD_REQUEST)
            if 'Development' not in details['CN']:
                return Response({'errors': 'This is not development certificate.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'errors': 'Certificate type is missed.'}, status=status.HTTP_400_BAD_REQUEST)

        path = os.path.join(settings.BASE_DIR, 'certs/', file_name)
        path_cert = os.path.join(settings.BASE_DIR, 'certs/', file_name+'_cert.pem')
        path_key = os.path.join(settings.BASE_DIR, 'certs/', file_name+'_key.pem')
        with open(path, 'wb+') as temp_file:
            for chunk in cert_file.chunks():
                temp_file.write(chunk)

        with open(path_cert, 'wb+') as temp_file:
            temp_file.write(cert_str)

        with open(path_key, 'wb+') as temp_file:
            temp_file.write(key_str)

        cert = Certificate(cert_type=(cert_type == 'product'), file_name=file_name, app=app, name=cert_file.name,
                           expiry_date=expiry_date, bundle_identifier=bundle_name)
        cert.save()

        return Response({'cert': CertificateSerializer(cert).data})

    def _remove_cert(self, certs):
        if certs:
            cert = certs[0]
            path = os.path.join(settings.BASE_DIR, 'certs/', cert.file_name)
            os.remove(path)
            cert.delete()
            return Response({'status': 'success'})
        else:
            return Response({'errors': "certification doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['delete'])
    def remove_prod_cert(self, request, pk=None):
        app = self.get_object()
        return self._remove_cert(Certificate.objects.filter(app=app, cert_type=True))


    @detail_route(methods=['delete'])
    def remove_dev_cert(self, request, pk=None):
        app = self.get_object()
        return self._remove_cert(Certificate.objects.filter(app=app, cert_type=False))

    @action()
    def post_word(self, request, pk=None):
        """
            post a translation to the app
        """
        app = self.get_object()
        word = request.DATA.get('word', False)
        translation = request.DATA.get('translation', False)
        lang = request.DATA.get('lang', False)
        # validate posted params
        errors = {}
        if not word:
            errors['word'] = 'Required'

        if not translation:
            errors['translation'] = 'Required'

        if not lang:
            errors['lang'] = 'Required'
        elif lang not in [lang1[0] for lang1 in LANG_CHOICES]:
            errors['lang'] = 'Unsupported Language'
        
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        word_obj, word_created = Word.objects.get_or_create(app=app, name=word)
        translation_obj, translation_created = LocalizedWord.objects.get_or_create(app=app, name=translation, lang=lang, word=word_obj)
        json = LocalizedWordSerializer(translation_obj).data
        json['word_created'] = word_created
        json['translation_created'] = translation_created

        return Response(json)

@api_view(['GET'])
def cert_download(request, format=None):
    """
    A simple ViewSet that for downloading cert certificate
    """
    token_id = request.QUERY_PARAMS.get('token')
    token = Token.objects.get(pk=token_id)
    if not token:
        return Response("Not Authorized", status=status.HTTP_401_UNAUTHORIZED)

    app_id = request.QUERY_PARAMS.get('app')
    app = App.objects.get(pk=int(app_id or -1))
    if not app:
        return Response("App ID is required", status=status.HTTP_400_BAD_REQUEST)

    if app.owner != token.user:
        return Response("Not Authorized", status=status.HTTP_401_UNAUTHORIZED)

    cert_id = request.QUERY_PARAMS.get('cert')
    cert = Certificate.objects.get(pk=int(cert_id or -1))
    if not cert:
        return Response("Certification ID is required", status=status.HTTP_400_BAD_REQUEST)

    if cert.app != app:
        return Response("Not Authorized", status=status.HTTP_401_UNAUTHORIZED)

    cert_file = open(os.path.join(settings.BASE_DIR, 'certs/', cert.file_name), 'rb')
    response = HttpResponse(FileWrapper(cert_file), content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="%s"' % cert.name

    return response


class WordViewSet(viewsets.ModelViewSet):
    serializer_class = WordSerializer
    model = Word
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Word.objects.filter(app__owner=self.request.user)


class LocalizedWordViewSet(viewsets.ModelViewSet):
    serializer_class = LocalizedWordSerializer
    model = LocalizedWord
    permission_classes = (permissions.IsAuthenticated,)

    @list_route(methods=['post'])
    def import_localwords(self, request):
        app = request.DATA.get('app', False)
        data = request.DATA.get('data', False)
        lang = request.DATA.get('lang', False)
        page_size = request.DATA.get('pz', 20)
        # validate posted params
        errors = {}
        if not app:
            errors['app'] = 'Required'

        if not lang:
            errors['lang'] = 'Required'
        elif lang not in [lang1[0] for lang1 in LANG_CHOICES]:
            errors['lang'] = 'Unsupported Language'

        if not data:
            errors['data'] = 'Required'

        if not errors:
            app = App.objects.get(pk=int(app))
            if app:
                for item in data:
                    w = item['word']
                    name = item['val']
                    word, created = Word.objects.get_or_create(app=app, name=w)
                    localword, created = LocalizedWord.objects.get_or_create(app=app, word=word, lang=lang)
                    localword.name = name
                    localword.save()

                return _local_word(app, page_size=page_size)
            else:
                errors['app'] = 'Not Found'

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


    def create(self, request, *args, **kwargs):
        app = request.DATA.get('app')
        word = request.DATA.get('word')
        lang = request.DATA.get('lang')
        name = request.DATA.get('name')
        localword, created = LocalizedWord.objects.get_or_create(app_id=app, word_id=word, lang=lang)
        localword.name = name
        localword.save()

        return Response(LocalizedWordSerializer(localword).data)

    def destroy(self, request, pk=None):
        localword = self.get_object()
        localword.delete()
        return Response({})

    def get_queryset(self):
        return LocalizedWord.objects.filter(app__owner=self.request.user)


def success(request, token_id):
    user_code = UserCode.objects.filter(pk=token_id).first()
    if user_code:
        user = user_code.user
        user.email_verified = True
        user.save()
        user_code.delete()

        return render(request, 'success.html', {'user': user})
    else:
        return render(request, 'success.html', {'user': False})


def reset_password(request, token_id):
    user_code = UserCode.objects.filter(pk=token_id).first()
    if user_code:
        user = user_code.user
        user.email_verified = True
        user.save()
        if request.POST and request.POST['new_password']:
            if request.POST['new_password'] == request.POST['confirm_password']:
                if len(request.POST['new_password']) > 3:
                    user.set_password(request.POST['new_password'])
                    user.save()
                    user_code.delete()

                    return render(request, 'reset_password.html', {'user': user, 'token': token_id, 'success': True})
                else:
                    return render(request, 'reset_password.html', {'user': user, 'token': token_id, 'error': True,
                                                            'msg': 'Password should be at least 4 characters long.'})
            else:
                return render(request, 'reset_password.html', {'user': user, 'token': token_id, 'error': True,
                                                                'msg': 'Please match passwords!'})

        return render(request, 'reset_password.html', {'user': user, 'token': token_id})
    else:
        return render(request, 'reset_password.html', {'user': False})

@api_view(['POST'])
def send_message(request):
    data = {
        'name': request.DATA.get('name'),
        'email': request.DATA.get('email'),
        'msg':  request.DATA.get('message')
    }

    plaintext = get_template('message.txt')
    htmly = get_template('message.html')
    d = Context(data)

    subject, from_email, to = '%s wrote you a note[InAppTranslation]' % data['email'], 'no-reply@inapptranslation.com', \
                              settings.SUPPORT_EMAIL
    text_content = plaintext.render(d)
    html_content = htmly.render(d)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return Response({'status': 'success'})


class TranslationListView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        token = request.QUERY_PARAMS.get('token', False)
        if not token:
            return Response({'errors': 'app token is required.'}, status=status.HTTP_400_BAD_REQUEST)

        udid = request.QUERY_PARAMS.get('udid', False)
        #if not udid:
        #    return Response({'errors': 'UDID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        app = App.objects.filter(token=token).first()
        if not app:
            return Response({'errors': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

        code = request.QUERY_PARAMS.get('lang', False)
        if code and code not in [lang[0] for lang in LANG_CHOICES]:
            return Response({'errors': 'lang code is not valid.'}, status=status.HTTP_400_BAD_REQUEST)

        if udid:
            r = redis.StrictRedis()
            flag = False
            reg_date = datetime.now().strftime('%Y-%m-%d')
            _key = '%s__%s__%s' % (reg_date, code, udid)
            if not r.get(_key):
                flag = True
            r.incrby(_key)
            if flag:
                daily_stats, created = DailyAppStats.objects.get_or_create(app=app, reg_date=reg_date, lang=code)
                daily_stats.hit_count += 1
                daily_stats.save()
                r.expire(_key, 3600*24)

            flag = False
            reg_month = datetime.now().strftime('%Y-%m')
            _key = '%s__%s__%s' % (reg_month, code, udid)
            if not r.get(_key):
                flag = True
            r.incrby(_key)
            if flag:
                monthly_stats, created = MonthlyAppStats.objects.get_or_create(app=app, reg_month=reg_month, lang=code)
                monthly_stats.hit_count += 1
                monthly_stats.save()
                r.expire(_key, 3600*24*30)

        last_fetch_datetime = request.META.get('HTTP_LAST_FETCH_DATETIME')
        # logging.debug(request.META)
        if last_fetch_datetime:
            last_fetch_datetime = datetime.strptime(last_fetch_datetime, '%Y-%m-%d %H:%M:%S')
            last_fetch_datetime = last_fetch_datetime.replace(tzinfo=pytz.UTC)
            if last_fetch_datetime >= app.updated:
                return Response({'updated': False, 'translations': []})



        _filter = {'app': app}
        if code:
            _filter['lang'] = code

        local_words = LocalizedWord.objects.filter(**_filter).all()

        res = {}
        for t in local_words:
            lang = t.lang
            if not res.get(lang, False):
                res[lang] = {}
            res[lang][t.word.name] = {'id': t.id, 'text': t.name}

        return Response({'updated': True, 'translations': [{'lang': lang, 'content': res[lang]} for lang in res]})


class AppSatisfiedApiView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        token = request.QUERY_PARAMS.get('token', False)
        lang = request.QUERY_PARAMS.get('lang', False)
        satisfied = request.QUERY_PARAMS.get('satisfied', False)
        if not token or not lang or not satisfied:
            return Response({'errors': 'app token, uuid, lang and satisfied("Y" or "N") are required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if lang not in [code[0] for code in LANG_CHOICES]:
            return Response({'errors': 'lang code is not valid.'}, status=status.HTTP_400_BAD_REQUEST)

        app = App.objects.filter(token=token).first()
        if not app:
            return Response({'errors': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)


        feedback, created = AppFeedback.objects.get_or_create(app=app, lang=lang)
        satisfied_count = 0 if created else feedback.satisfied
        unsatisfied_count = 0 if created else feedback.unsatisfied
        if satisfied == 'Y':
            satisfied_count += 1
        else:
            unsatisfied_count += 1

        feedback.satisfied = satisfied_count
        feedback.unsatisfied = unsatisfied_count
        feedback.save()

        return Response({'status': 'ok'})


class TranslationUnsatisfiedApiView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        token = request.QUERY_PARAMS.get('token', False)

        satisfied_word_ids = request.QUERY_PARAMS.get('s_word_ids', '')
        unsatisfied_word_ids = request.QUERY_PARAMS.get('u_word_ids', '')
        lang = request.QUERY_PARAMS.get('lang', False)

        if lang not in [code[0] for code in LANG_CHOICES]:
            return Response({'errors': 'lang code is not valid.'}, status=status.HTTP_400_BAD_REQUEST)

        app = App.objects.filter(token=token).first()
        if not app:
            return Response({'errors': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

        """
            return int
            0: success
            1: feedback was set by that user
            2: invalid
        """
        def update_lw_feedback(word_id, satisified):
            local_word = LocalizedWord.objects.filter(id=word_id, app=app).first()
            if not local_word:
                return 2

            lw_feedback, created = LocalizedWordFeedback.objects.get_or_create(app=app, word=local_word.word, lang=lang)
            satisfied_count = 0 if created else lw_feedback.satisfied
            unsatisfied_count = 0 if created else lw_feedback.unsatisfied
            if satisified:
                satisfied_count += 1
            else:
                unsatisfied_count += 1
            lw_feedback.satisfied = satisfied_count
            lw_feedback.unsatisfied = unsatisfied_count
            lw_feedback.save()

            return 0

        res = [0, 0, 0]
        if satisfied_word_ids:
            ids = satisfied_word_ids.split(',')
            for id in ids:
                res[update_lw_feedback(id, True)] += 1

        if unsatisfied_word_ids:
            ids = unsatisfied_word_ids.split(',')
            for id in ids:
                res[update_lw_feedback(id, False)] += 1

        return Response({'status': 'ok', 'success': res[0],  'invalid': res[2]})


class AppDetailApiView(generics.CreateAPIView):
    serializer_class = AppDetailSerializer
    def post(self, request, *args, **kwargs):
        app_id = request.DATA.get('app_id')
        if not app_id:
            return Response({'errors': 'app_id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        r = requests.get("http://itunes.apple.com/lookup?id=%s" % app_id)
        if r.status_code == 200:
            d = json.loads(r.content, 'utf-8')
            if d.get('resultCount') and d['results'][0]:
                res = {}
                res['logo'] = d['results'][0]['artworkUrl512']
                res['screenshot'] = d['results'][0]['screenshotUrls'][0]
                return Response({'results': res})
            else:
                return Response({'errors': 'Invalid link.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'errors': 'Invalid link.'}, status=status.HTTP_400_BAD_REQUEST)


class AddKeyApiView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        token = request.QUERY_PARAMS.get('token', False)
        key = request.QUERY_PARAMS.get('key', '')

        app = App.objects.filter(token=token).first()
        if not app:
            return Response({'errors': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

        word, created = Word.objects.get_or_create(app=app, name=key)

        return Response({'status': 'created' if created else 'exist'})