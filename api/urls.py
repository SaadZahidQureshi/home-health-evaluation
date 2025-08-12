from django.urls import path
from rest_framework import routers
from api.user.views import *
from api.home.views import *
router = routers.DefaultRouter(trailing_slash=False)

router.register(r"user", UserViewSet, basename="user")
router.register(r"principles", PrincipleViewSet, basename="principles")
router.register(r"categories", CategoriesViewSet, basename="categories")
router.register(r"pesttypes", PestTypeViewSet, basename="pesttypes")
router.register(r"questiongroups", QuestionGroupViewSet, basename="questiongroups")
router.register(r"questions", QuestionViewSet, basename="questions")
router.register(r"answers", AnswerViewSet, basename="answers")
router.register(r"photos", PhotosViewSet, basename="photos")
router.register(r"customers", CustomerViewSet, basename="customers")


urlpatterns = [
    path("login", LoginUserAPIView.as_view(), name="login"),
    path("logout", LogoutAPIView.as_view(), name="logout"),
    path("me", MeAPIView.as_view(), name="me"),
] + router.urls


