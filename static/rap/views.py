from django.shortcuts import render
from rest_framework import permissions, generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from . import serializers
from .permissions import IsAccountOwner
from .send_email import send_confirmation_email, send_code_password_reset
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserListSerializer
from EducateApi.tasks import send_email_task

User = get_user_model()


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (permissions.AllowAny,)


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsAccountOwner)
    serializer_class = serializers.UserDetailSerializer


class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                # send_confirmation_email(user.email)
                send_email_task.delay(user.email)
            return Response(serializer.data, status=201)
        return Response('Bad request!', status=400)


class LoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)


class LogoutView(GenericAPIView):
    serializer_class = serializers.LogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Successfully logged out!', status=204)


class ForgotPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.ForgotPasswordSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            email = serializer.data.get('email')
            user = User.objects.get(email=email)
            user.create_activation_code()
            user.save()
            send_code_password_reset(user)
            return Response('Check your email, we send a code!', status=200)
        except User.DoesNotExist:
            return Response('User with this email does not exists!', status=400)


class RestorePasswordView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.RestorePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Password changed successfully!')


def auth(request):
    return render(request, 'oauth.html')


class FollowSpamApi(APIView):
    def post(self, request):
        serializer = serializers.SpamViewSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(email=request.user.email)
        return Response('Followed to spam!', 201)
