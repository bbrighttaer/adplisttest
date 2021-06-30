from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import render
from django.utils.encoding import DjangoUnicodeDecodeError, smart_bytes, smart_str
import drf_yasg
from rest_framework import generics, serializers, status, views
from .serializers import (RegisterSerializer, EmailVerificationSerializer, LoginSerializer,
                          ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer,
                          RequestEmailVerificationSerializer)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .renderers import UserRenderer
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# Create your views here.

def send_verification_link(user, request):
    token = RefreshToken.for_user(user).access_token

    current_site = get_current_site(request).domain
    relative_link = reverse('email-verify')

    absurl = 'https://' + current_site + \
        relative_link + "?token=" + str(token)
    email_body = 'Hi ' + user.username + \
        ',\nUse the link below to verify your email \n' + absurl
    data = {
        'email_body': email_body,
        'email_subject': 'Verify your email',
        'to_email': user.email
    }

    Util.send_email(data)

class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer, )

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        send_verification_link(user, request)

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):

    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY,
                                           description='Activation token',
                                           type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        print(token)
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({
                'email': 'Successfully activated'
            }, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as e:
            return Response({
                'error': 'Activation Expired'
            },
                status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError as e:
            return Response({
                'error': 'Invalid token'
            },
                status=status.HTTP_400_BAD_REQUEST)


class RequestEmailVerifyAPIView(views.APIView):

    serializer_class = RequestEmailVerificationSerializer

    @swagger_auto_schema(responses={200: 'Success'},
                         request_body=RequestEmailVerificationSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data['email']
        if email and User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            send_verification_link(user, request)     

        return Response({"success": "Verfication email has been sent to your inbox"},
                        status=status.HTTP_200_OK)


class LoginAPIView(generics.GenericAPIView):

    serializer_class = LoginSerializer
    renderer_classes = (UserRenderer, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):

    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class()

        data = request.data
        email = data['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request).domain
            relative_link = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            absurl = 'http://' + current_site + relative_link
            email_body = 'Hi ' + user.username + \
                ',\n\nUse the link below to reset your password \n' + absurl
            data = {
                'email_body': email_body,
                'email_subject': 'Reset Password',
                'to_email': user.email
            }

        Util.send_email(data)

        return Response({'success': 'We have sent you a link to reset your password'},
                        status=status.HTTP_200_OK)


class PasswordTokenCheckAPIView(generics.GenericAPIView):

    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'},
                                status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success': True,
                             'message': 'Credentials valid',
                             'uidb64': uidb64,
                             'token': token
                             },
                            status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as e:
            return Response({'error': 'Token is not valid, please request a new one'},
                            status=status.HTTP_401_UNAUTHORIZED)


class SetNewPassWordAPIView(generics.GenericAPIView):

    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'},
                        status=status.HTTP_200_OK)
