from authentication.utils import EXPERTISE, MENTORSHIP_AREAS, TITLE, MENTOR_STATUS, USER_TYPE
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework import fields
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, *args, **kwargs):
        email = kwargs.pop('email') if 'email' in kwargs else None
        password = kwargs['password'] if 'password' in kwargs else None
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        if 'joined_as' in kwargs and kwargs['joined_as'] == 'mentor':
            user.mentor_status = 'pending'
        user.save()
        return user

    def create_superuser(self, *args, **kwargs):
        user = self.create_user( *args, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    # User demographics
    title = models.CharField(max_length=5, choices=TITLE)
    username = models.CharField(max_length=255, unique=True, db_index=True)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    location = models.CharField(max_length=255)
    employer = models.CharField(max_length=50)
    expertise = models.CharField(max_length=555, blank=True, null=True)
    joined_as = models.CharField(default='member', choices=USER_TYPE, max_length=10)
    mentor_status = models.CharField(default='not applicable', choices=MENTOR_STATUS, max_length=20)

    # Applicable to mentors only
    mentorship_areas = models.CharField(max_length=555, blank=True, null=True)

    # Internal records keeping
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName', 'username', 'location']

    objects = UserManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.mentorship_areas and isinstance(self.mentorship_areas, str):
            self.mentorship_areas = eval(self.mentorship_areas)
        if self.expertise and isinstance(self.expertise, str):
            self.expertise = eval(self.expertise)

    def __str__(self) -> str:
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
