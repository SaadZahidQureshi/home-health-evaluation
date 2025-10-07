from django.shortcuts import render

# Create your views here.
from django.contrib.auth import get_user_model, login, logout
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin

from api.administration.serializers import LoginAdminSerializer
from api.core.permissions import AdminPermission
from api.user.serializers import *
from api.user.models import *
from api.core.pagination import Pagination
from api.core.mixin import DotsModelViewSet, GenericDotsViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import TokenManagement
from .serializers import TokenSerializer, TokenRegenerateSerializer, AdminUpdateSerializer

User = get_user_model()


class AdminViewSet(DotsModelViewSet):
    queryset = User.objects.filter(role=Roles.ADMIN)
    serializer_class = UserSerializer
    serializer_create_class = AdminUpdateSerializer
    permission_classes = [AllowAny]
    pagination_class = Pagination
    
    @action(detail=False, methods=["POST"], url_path="login", permission_classes=[AllowAny])
    def user_login(self, request, *args, **kwargs):
        serializer = LoginAdminSerializer(data=self.request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["POST"], url_path="logout", permission_classes=[IsAuthenticated])
    def user_logout(self, request, *args, **kwargs):
        logout(self.request)
        request.session.flush()
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["GET"], url_path="me", permission_classes=[IsAuthenticated])
    def me(self, request, *args, **kwargs):
        serializer = UserSerializer(self.request.user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenManagementViewSet(DotsModelViewSet):
    queryset = TokenManagement.objects.all().order_by("-created_at")
    serializer_class = TokenSerializer
    permission_classes = [AdminPermission]
    search_fields = ["email"]


    @action(detail=False, methods=["POST"], url_path="regenerate", serializer_class=TokenRegenerateSerializer)
    def regenerate(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.save()
        return Response(TokenSerializer(token).data, status=status.HTTP_201_CREATED)
    

class UserManagementViewSet(GenericDotsViewSet, ListModelMixin):
    queryset = User.objects.filter(role=Roles.USER).order_by("-created_at")
    serializer_class = UserSerializer
    permission_classes = [AdminPermission]
    pagination_class = Pagination
    search_fields = ["email", "name", "phone"]

