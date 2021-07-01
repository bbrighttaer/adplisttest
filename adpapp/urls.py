from django.urls import path
from .views import (OnBoardingDataAdminAPIView, OnBoardingDataAPIView, 
                    UserProfileUpdateAPIView, MentorsListAPIView,
                    UserListAPIView, MembersListAPIView)


urlpatterns = [
    path('onboarding/<int:id>/', OnBoardingDataAdminAPIView.as_view(), name='onboarding-detailed'),
    path('onboarding/', OnBoardingDataAPIView.as_view(), name='onboarding'),
    path('profile/<id>', UserProfileUpdateAPIView.as_view(), name='profile'),
    path('users/', UserListAPIView.as_view(), name='users-list'),
    path('users/mentors/', MentorsListAPIView.as_view(), name='mentor-list'),
    path('users/members/', MembersListAPIView.as_view(), name='member-list'),

]
