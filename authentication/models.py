from authentication.utils import EXPERTISE, MENTORSHIP_AREAS, TITLE
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

        # if username is None:
        #     raise TypeError('Users should have a username')

        # if email is None:
        #     raise TypeError('Users should have a Email')

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, *args, **kwargs):
        # if username is None:
        #     raise TypeError('Users should have a username')

        # if password is None:
        #     raise TypeError('Users should not be empty')

        # if email is None:
        #     raise TypeError('Users should have a Email')

        user = self.create_user(*args, **kwargs)
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
    expertise = models.CharField(max_length=555, blank=True)
    is_mentor = models.BooleanField(default=False)

    # False always for a member (assumes that a user cannot be a member and a mentor simultaneously)
    is_mentor_approved = models.BooleanField(default=False)

    # Applicable to mentors only
    mentorship_areas = models.CharField(max_length=555, blank=True)

    # Internal records keeping
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['firstName', 'lastName', 'email', 'location']

    objects = UserManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.mentorship_areas and isinstance(self.mentorship_areas, str):
            self.mentorship_areas = eval(self.mentorship_areas)
        if self.expertise and isinstance(self.expertise, str):
            self.expertise = eval(self.expertise)

    def __str__(self) -> str:
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
