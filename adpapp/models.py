from django.db import models

from authentication.utils import USER_TYPE

# Create your models here.

class OnBoardingData(models.Model):

    info_type = models.CharField(max_length=32)
    content = models.CharField(max_length=555)
    user_type = models.CharField(max_length=20, choices=USER_TYPE)

    class Meta:
        ordering = ['user_type']