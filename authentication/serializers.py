from authentication.utils import EXPERTISE, MENTORSHIP_AREAS
from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from password_strength import PasswordPolicy
from rest_framework import fields

password_policy = PasswordPolicy.from_names(
    length=6,  # min length: 6
    uppercase=1,  # need min. 1 uppercase letters
    numbers=1,  # need min. 1 digits
    special=1,  # need min. 1 special characters
)


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    is_staff = serializers.BooleanField(default=False, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    expertise = fields.MultipleChoiceField(choices=EXPERTISE, allow_blank=True)
    mentorship_areas = fields.MultipleChoiceField(choices=MENTORSHIP_AREAS, allow_blank=True)

    class Meta:
        model = User
        fields = ['title', 'username', 'firstName', 'lastName',
                  'email',  'password', 'location', 'employer',
                  'expertise', 'is_mentor', 'mentorship_areas',
                  'expertise', 'is_staff', 'created_at', 'updated_at']

    def validate(self, attrs):        
        def get_param(x): return attrs.get(x, None)

        # attributes
        password = get_param('password')
        is_mentor = get_param('is_mentor')
        mentorship_areas = get_param('mentorship_areas')
        expertise = get_param('expertise')

        # if not username.isalnum():
        #     raise serializers.ValidationError(
        #         'The username should only contain alphanumeric characters')

        # Password strength check
        if len(password_policy.test(password)) > 0:
            raise serializers.ValidationError('The password must have a minimum size of 6 and contain at '
                                              + 'least 1 uppercase letter, 1 number, and 1 special character')

        # Mentorship areas check for mentors
        if is_mentor and not mentorship_areas:
            raise serializers.ValidationError(
                'mentorship_areas property is required for mentors')

        # Expertise property check for mentors
        if is_mentor and not expertise:
            raise serializers.ValidationError(
                'expertise property is required for mentors')

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):

    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']

class RequestEmailVerificationSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=555, min_length=5)

    class Meta:
        model = User
        fields = ['email']


class LoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=6, read_only=True)
    tokens = serializers.CharField(max_length=555, min_length=6, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')

        if not user.is_active:
            raise AuthenticationFailed(
                'Account disabled, contact adinistrator')

        if not user.is_verified:
            raise AuthenticationFailed('Account is not verified')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens()
        }


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        return super().validate(attrs)


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, max_length=555)
    uidb64 = serializers.CharField(min_length=1, max_length=68)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            if len(password_policy.test(password)) > 0:
                raise serializers.ValidationError('The password must have a minimum size of 6 and contain at '
                                                + 'least 1 uppercase letter, 1 number, and 1 special character')

            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)
