from rest_framework import response
from adpapp.permissions import IsOwnerOrSuperuser
from authentication.utils import EXPERTISE, USER_TYPE, MENTOR_STATUS
from django.shortcuts import render
from rest_framework import views, generics, status, permissions
from rest_framework.response import Response
from .models import OnBoardingData
from .serializers import OnBoardingDataSerializer, UserProfileSerializer
from authentication.renderers import OutBoundDataRenderer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from authentication.models import User

# Create your views here.


class OnBoardingDataAPIView(generics.ListCreateAPIView):

    serializer_class = OnBoardingDataSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [OutBoundDataRenderer]

    user_type_param_config = openapi.Parameter('user_type', in_=openapi.IN_QUERY,
                                               description='User type',
                                               enum=[c for _, c in USER_TYPE],
                                               type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[user_type_param_config], responses={200: 'success'})
    def get(self, request):
        user_type = request.GET.get('user_type')
        data = OnBoardingData.objects.filter(user_type=user_type)
        serializer = self.serializer_class(data, many=True)
        return Response({'onboarding': serializer.data}, status=status.HTTP_200_OK)


class OnBoardingDataAdminAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = OnBoardingDataSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    renderer_classes = [OutBoundDataRenderer]
    queryset = OnBoardingData.objects.all()
    lookup_field = 'id'


class UserProfileUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSuperuser]
    renderer_classes = [OutBoundDataRenderer]
    queryset = User.objects.all()
    lookup_field = 'id'


class UserListAPIView(generics.ListAPIView):

    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    renderer_classes = [OutBoundDataRenderer]
    queryset = User.objects.all()

    filter_param_config = openapi.Parameter('filter', in_=openapi.IN_QUERY,
                                            description='Select a subset of users based on their expertise',
                                            enum=[c for _, c in EXPERTISE],
                                            type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[filter_param_config],
                         response=UserProfileSerializer)
    def get(self, request):
        filter_opt = request.GET.get('filter')
        selected = self.get_queryset().filter(
            expertise__contains=filter_opt) if filter_opt else self.get_queryset()
        serializer = self.serializer_class(selected, many=True)
        return Response({'results': serializer.data}, status=status.HTTP_200_OK)


class MembersListAPIView(UserListAPIView):
    queryset = User.objects.filter(joined_as='member')
    filter_param_config = openapi.Parameter('filter', in_=openapi.IN_QUERY,
                                            description='Select a subset of members/mentees based on their expertise',
                                            enum=[c for _, c in EXPERTISE],
                                            type=openapi.TYPE_STRING)
    
    @swagger_auto_schema(manual_parameters=[filter_param_config],
                         response=UserProfileSerializer)
    def get(self, request):
        return super().get(request)

class MentorsListAPIView(UserListAPIView):
    queryset = User.objects.filter(joined_as='mentor')
    filter_param_config = openapi.Parameter('filter', in_=openapi.IN_QUERY,
                                            description='Select a subset of mentors based on their expertise',
                                            enum=[c for _, c in MENTOR_STATUS],
                                            type=openapi.TYPE_STRING)
    
    @swagger_auto_schema(manual_parameters=[filter_param_config],
                         response=UserProfileSerializer)
    def get(self, request):
        filter_opt = request.GET.get('filter')
        selected = self.get_queryset().filter(
            mentor_status=filter_opt) if filter_opt else self.get_queryset()
        serializer = self.serializer_class(selected, many=True)
        return Response({'results': serializer.data}, status=status.HTTP_200_OK)