from django.urls import path
from rest_framework import routers
from api.user.views import UserViewSet, LoginUserViewSet
router = routers.DefaultRouter(trailing_slash=False)

router.register(r"user", UserViewSet, basename="register")

urlpatterns = [
    path("login", LoginUserViewSet.as_view(), name="login")
] + router.urls


