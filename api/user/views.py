from django.contrib.auth import get_user_model, login
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from . serializers import LoginUserSerializer, RegisterUserSerializer, UserSerializer
from api.core.pagination import Pagination
from api.core.mixin import DotsModelViewSet
User = get_user_model()

class UserViewSet(DotsModelViewSet):
    queryset = User.objects.all().exclude(role="admin")
    serializer_class = UserSerializer
    serializer_create_class = RegisterUserSerializer
    permission_classes = [AllowAny]
    pagination_class = Pagination


class LoginUserViewSet(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginUserSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(status=status.HTTP_200_OK)

