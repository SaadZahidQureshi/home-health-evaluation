from django.urls import path
from rest_framework import routers
from api.user.views import *
from api.home.views import *
router = routers.DefaultRouter(trailing_slash=False)

router.register(r"user", UserViewSet, basename="user")
router.register(r"principles", PrincipleViewSet, basename="principles")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"photos", PhotoViewSet, basename="photos")
router.register(r"customers", CustomerViewSet, basename="customers")
router.register(r"feedbacks", FeedbackViewSet, basename="feedbacks")

urlpatterns = [
    
] + router.urls


