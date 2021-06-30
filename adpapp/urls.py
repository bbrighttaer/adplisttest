from django.urls import path
from .views import OnBoardingDataAdminAPIView, OnBoardingDataAPIView


urlpatterns = [
    path('onboarding/<int:id>/', OnBoardingDataAdminAPIView.as_view(), name='onboarding-detailed'),
    path('onboarding/', OnBoardingDataAPIView.as_view(), name='onboarding'),
]
