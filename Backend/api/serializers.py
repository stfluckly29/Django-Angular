from rest_framework import serializers
from .models import User, App, Word, LocalizedWord, Certificate
from rest_framework.authtoken.models import Token
import re

class WordSerializer(serializers.ModelSerializer):

    def validate_app(self, attrs, source):
        """
            Check the submitted app is related to logged in user
        """
        value = attrs[source]
        view = self.context['view']
        if value.owner != view.request.user:
            raise serializers.ValidationError("App is not belonged to logged in user.")

        return attrs

    class Meta:
        model = Word


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate


class AppSerializer(serializers.ModelSerializer):
    total_count = serializers.SerializerMethodField(method_name="get_total_count")
    certs = serializers.SerializerMethodField(method_name="get_certs")

    class Meta:
        model = App
        read_only_fields = ('owner',)
        fields = ('id', 'name', 'owner', 'total_count', 'enabled', 'certs', 'token', 'logo', 'screenshot', 'app_id',
                  'updated')

    def get_total_count(self, obj):

        return LocalizedWord.objects.filter(word__app=obj).count()

    def get_certs(self, obj):
        certs = Certificate.objects.filter(app=obj).order_by('cert_type')
        serializer = CertificateSerializer(certs, many=True)

        return serializer.data


class AppListField(serializers.RelatedField):
    def to_native(self, value):
        json = {}
        json['id'] = value.id
        json['name'] = value.name
        json['count'] = LocalizedWord.objects.filter(word__app=value).count()

        return json


class UserSerializer(serializers.ModelSerializer):
    #apps = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                               #view_name='app-detail')
    #apps = AppListField(many=True)
    token = serializers.SerializerMethodField('get_token')
    password = serializers.CharField(required=False, write_only=True)
    avatar = serializers.SerializerMethodField('get_avatar')

    class Meta:
        model = User
        fields = ('id', 'company', 'username', 'password', 'token', 'is_superuser', 'avatar')
        # write_only_fields = ('password',)

    def validate_username(self, attrs, instance=None):
        """
            Check the submitted username is valid email
        """
        email = attrs['username']
        pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(pattern, email):
            raise serializers.ValidationError("Please input valid email address.")

        return attrs

    def restore_object(self, attrs, instance=None):
        # call set_password on user object. Without this
        # the password will be stored in plain text.
        user = super(UserSerializer, self).restore_object(attrs, instance)
        if attrs.get('password', False):
            user.set_password(attrs['password'])
        return user

    def get_token(self, obj):
        return Token.objects.get_or_create(user=obj)[0]

    def get_avatar(self, instance):
        return self.context['request'].build_absolute_uri(instance.avatar.url) if instance.avatar else ''

class WordName(serializers.RelatedField):
    def to_native(self, value):
        return value.name

        return json


class LocalizedWordSerializer(serializers.ModelSerializer):
    def validate_app(self, attrs, source):
        """
            Check the submitted app is related to logged in user
        """
        value = attrs[source]
        view = self.context['view']
        if value.owner != view.request.user:
            raise serializers.ValidationError("App is not belonged to logged in user.")

        return attrs

    def validate_word(self, attrs, source):
        """
            Check the submitted word is related to submitted app
        """
        app = attrs['app']
        word = attrs['word']
        if word.app.id != app.id:
            raise serializers.ValidationError("Word is not belonged to submitted app.")

        return attrs

    class Meta:
        model = LocalizedWord


class AppDetailSerializer(serializers.Serializer):
    link = serializers.CharField(max_length=200)