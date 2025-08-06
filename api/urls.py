from django.urls import path
from rest_framework import routers
from api.user.views import UserViewSet, LoginUserAPIView, MeAPIView, LogoutAPIView
router = routers.DefaultRouter(trailing_slash=False)

router.register(r"user", UserViewSet, basename="register")

urlpatterns = [
    path("login", LoginUserAPIView.as_view(), name="login"),
    path("logout", LogoutAPIView.as_view(), name="logout"),
    path("me", MeAPIView.as_view(), name="me"),
] + router.urls


