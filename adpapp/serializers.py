
from authentication.utils import EXPERTISE, MENTORSHIP_AREAS
from rest_framework import serializers
from .models import OnBoardingData
from authentication.models import User
from rest_framework import fields


class OnBoardingDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = OnBoardingData
        exclude = []


class UserProfileSerializer(serializers.ModelSerializer):

    expertise = fields.MultipleChoiceField(choices=EXPERTISE, allow_blank=True)
    mentorship_areas = fields.MultipleChoiceField(
        choices=MENTORSHIP_AREAS, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'title', 'username', 'firstName', 'lastName',
                  'email', 'location', 'employer', 'expertise',
                  'mentorship_areas', 'expertise', 'joined_as', 'mentor_status']
