
from rest_framework import serializers
from .models import OnBoardingData
from authentication.models import User

class OnBoardingDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = OnBoardingData
        exclude = []