from authentication.utils import USER_TYPE
from django.shortcuts import render
from rest_framework import views, generics, status, permissions
from rest_framework.response import Response
from .models import OnBoardingData
from .serializers import OnBoardingDataSerializer
from authentication.renderers import OutBoundDataRenderer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

class OnBoardingDataAPIView(generics.ListCreateAPIView):

    serializer_class = OnBoardingDataSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [OutBoundDataRenderer]
    
    user_type_param_config = openapi.Parameter('user_type', in_=openapi.IN_QUERY,
                                           description='User type',
                                           enum=[c for c, _ in USER_TYPE],
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

    
