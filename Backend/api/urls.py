from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import *
from rest_framework.authtoken import views
from GengoApi import *

router = DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet)
router.register(r'apps', AppViewSet)
router.register(r'words', WordViewSet)
router.register(r'translations', LocalizedWordViewSet)

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls))
)

urlpatterns += [
    url(r'^m_translations/$', TranslationListView.as_view(), name='translation-list'),
    url(r'^m_app_feedback/$', AppSatisfiedApiView.as_view(), name='app-satisfied'),
    url(r'^m_word_feedback/$', TranslationUnsatisfiedApiView.as_view(), name='translation-unsatisfied'),
    url(r'^m_add_key/$', AddKeyApiView.as_view(), name='add-key'),
    url(r'app/lookup/$', AppDetailApiView.as_view(), name='app-detail-view'),

    url(r'^api-token-auth', 'api.views.modified_obtain_auth_token'),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^registration/(?P<token_id>\w+)/$', 'api.views.success', name='success'),
    url(r'^password_reset/(?P<token_id>\w+)/$', 'api.views.reset_password', name='reset_password'),
    url(r'^send-message/$', 'api.views.send_message', name='send_message'),
    url(r'^cert-download/$', cert_download),

    url(r'current_user/update', CurrentUserUpdateView.as_view(), name='change-avatar'),
    url(r'gengo/jobs/$', GengoPostApiView.as_view(), name='gengo-post'),
    url(r'gengo/callback/(?P<app_id>\w+)/(?P<word_id>\w+)/(?P<lang_code>\w+)/$', GengoCallbackAPIView.as_view(),
        name='gengo-callback')
]