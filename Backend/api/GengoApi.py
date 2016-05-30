from rest_framework import status
from .models import *
from rest_framework.response import Response
from gengo import Gengo
from rest_framework import generics
from slugify import slugify
from models import LANG_CHOICES
from django.core.urlresolvers import reverse
import cgi
import json
from rest_framework import permissions
from .serializers import LocalizedWordSerializer
import logging

#logging.basicConfig(filename='inapp.log', level=logging.DEBUG)

not_supported = ['ca', 'hr']
variation = {
	'zh-hans': 'zh',
	'zh-hant': 'zh-tw',
	'en-au': 'en-gb',
	'hu': 'h',
	'es-mx': 'es-la',
	'nb': 'no',
	'pt-pt': 'pt',
	'ru': 'r'
}


class GengoPostApiView(generics.CreateAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = LocalizedWordSerializer

	def post(self, request, *args, **kwargs):
		gengo = Gengo(
			public_key=settings.GENGO_PUBLIC_KEY,
			private_key=settings.GENGO_PRIVATE_KEY,
			sandbox=settings.GENGO_SANDBOX,
			debug=settings.GENGO_DEBUG)

		app_id = request.DATA.get('app')
		lang_code = request.DATA.get('lang', '')
		tier = request.DATA.get('tier', 'standard')
		comment = request.DATA.get('comment', '')

		app = App.objects.filter(pk=app_id).first()
		if not app:
			return Response({'errors': 'app_id is not valid.'}, status=status.HTTP_400_BAD_REQUEST)

		if lang_code and lang_code not in [lang[0] for lang in LANG_CHOICES]:
			return Response({'errors': 'lang code is not valid.'}, status=status.HTTP_400_BAD_REQUEST)
		lang_code = lang_code.lower()
		if lang_code in not_supported:
			return Response({'errors': 'Not Supported Language.'}, status=status.HTTP_400_BAD_REQUEST)

		if lang_code in variation:
			lang_code = variation[lang_code]

		if tier not in ['standard', 'pro']:
			return Response({'errors': 'tier is not valid.'}, status=status.HTTP_400_BAD_REQUEST)

		words = Word.objects.filter(app=app).all()

		jobs = {}
		for i in range(len(words)):
			k = 'job_%s' % (i + 1)
			word = words[i]
			cb = settings.DOMAIN + reverse('gengo-callback', kwargs=dict(app_id=app.id, word_id=word.id,
			                                                             lang_code=request.DATA.get('lang', '')))

			job = {
				'type': 'text',
				'slug': slugify(word.name),
				'body_src': word.name,
				'lc_src': 'en',
				'lc_tgt': lang_code,
				'tier': tier,
				'auto_approve': 1,
				'comment': '',
				'attachments': [],
				'callback_url': cb,
				'custom_data': '',
				'force': 0,
				'use_preferred': 0
			}
			jobs[k] = job

		jobs['comment'] = comment
		res = gengo.postTranslationJobs(jobs=jobs)

		return Response(data=res)


class GengoCallbackAPIView(generics.CreateAPIView):
	serializer_class = LocalizedWordSerializer

	def post(self, request, *args, **kwargs):
		app_id = self.kwargs.get('app_id')
		word_id = self.kwargs.get('word_id')
		lang_code = self.kwargs.get('lang_code')
		job = request.DATA.get('job')
		#logging.debug(app_id)
		#logging.debug(word_id)
		#logging.debug(lang_code)
		#logging.debug(job)
		job = json.loads(job, 'utf-8')
		if job.get('status') == 'approved':
			#logging.debug(job)
			lw, created = LocalizedWord.objects.get_or_create(app_id=app_id, word_id=word_id, lang=lang_code)
			lw.name = job.get('body_tgt')
			#logging.debug(lw.name)
			lw.save()

		return Response({'status': 'ok'}, status=status.HTTP_200_OK)