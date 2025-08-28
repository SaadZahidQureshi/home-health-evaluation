from django.contrib.auth import get_user_model, login, logout
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from . models import *
from . serializers import *
from api.core.pagination import Pagination
from api.core.mixin import DotsModelViewSet
User = get_user_model()

class UserViewSet(DotsModelViewSet):
    queryset = User.objects.all().exclude(role="admin")
    serializer_class = UserSerializer
    serializer_create_class = RegisterUserSerializer
    permission_classes = [AllowAny]
    pagination_class = Pagination

    @action(detail=False, methods=["PATCH"], url_path="password/update", permission_classes=[IsAuthenticated])
    def update_password(self, request, *args, **kwargs):
        serializer = UpdatePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.update(request.user, serializer.validated_data)
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["POST"], url_path="login", permission_classes=[AllowAny])
    def user_login(self, request, *args, **kwargs):
        serializer = LoginUserSerializer(data=self.request.data, context={'request': request})
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
    

class CustomerViewSet(DotsModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = ReturnCustomerSerializer
    serializer_create_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset().filter(created_by=self.request.user)
        if self.action in ["list"]:
            queryset = queryset.filter(audit_completed=True)
        return queryset

    def _get_customer(self, customer_id):
        try:
            return Customer.objects.get(id=customer_id)
        except (Customer.DoesNotExist, ValueError, TypeError):
            return None
        
    def get_or_create_customer(self, customer_id=None):
        if customer_id:
            customer = self._get_customer(customer_id)
            if customer:
                return customer
        current_user = self.request.user
        return Customer.create_default_customer(current_user)
    
    def create(self, request, *args, **kwargs):
        if not request.data:
            customer = self.get_or_create_customer()
            serializer = self.get_serializer(customer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['created_by'] = request.user
        
        if 'address' not in serializer.validated_data:
            serializer.validated_data['address'] = None
        if 'city' not in serializer.validated_data:
            serializer.validated_data['city'] = None
        if 'state' not in serializer.validated_data:
            serializer.validated_data['state'] = None
        if 'zip' not in serializer.validated_data:
            serializer.validated_data['zip'] = None
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PhotoViewSet(DotsModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]

