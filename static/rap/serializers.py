from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Spam_Contacts
User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'photo')


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['bought_courses'] = instance.UsersCourseView
        return repr


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=20, required=True, write_only=True)
    password2 = serializers.CharField(min_length=8, max_length=20,
                                      required=True, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'last_name', 'first_name', 'photo', 'about_user')

    def validate(self, attrs):
        password2 = attrs.pop('password2')
        if attrs['password'] != password2:
            raise serializers.ValidationError('Пароли не совпадают!')
        if not attrs['password'].isalnum():
            raise serializers.ValidationError('Пароль должен содержать буквенные и численные значения!')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  # **validated_data - все поля, которые мы заполняли в постмэне
        return user


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {'bad_token': _('Token is invalid or expired!')}

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class ForgotPasswordSerializers(serializers.Serializer):
    email = serializers.EmailField(max_length=100, required=True)


class RestorePasswordSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(min_length=8, required=True)
    password2 = serializers.CharField(min_length=8, required=True)

    def validate(self, attrs):
        password2 = attrs.pop('password2')
        if password2 != attrs['password']:
            raise serializers.ValidationError('Passwords didn\'t match!')
        try:
            user = User.objects.get(
                activation_code=attrs['code']
            )
        except User.DoesNotExist:
            raise serializers.ValidationError('Your code is incorrect!')
        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        user = data['user']
        user.set_password(data['password'])
        user.activation_code = ''
        user.save()
        return user


class SpamViewSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField()

    class Meta:
        model = Spam_Contacts
        fields = '__all__'

    def validate(self, attrs):
        email = self.context['request'].user.email
        if Spam_Contacts.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'You are already followed to spam!!'
            )
        return attrs

# TODO celery-cash
