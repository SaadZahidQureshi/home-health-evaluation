from django.urls import path
from rest_framework import routers
from api.user.views import *
from api.home.views import *
from api.home_energy.views import *
router = routers.DefaultRouter(trailing_slash=False)

router.register(r"user", UserViewSet, basename="user")
router.register(r"principles", PrincipleViewSet, basename="principles")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"photos", PhotoViewSet, basename="photos")
router.register(r"customers/healthy-home", HealthyHomeCustomer, basename="customers-healthy-home")
router.register(r"customers/residential-home", ResidentialHomeCustomer, basename="customers-residential-home")
router.register(r"feedbacks", FeedbackViewSet, basename="feedbacks")
# home energy views
router.register(r"steps", StepViewSet, basename="steps")
router.register(r"question", QuestionsViewSet, basename="questions")
router.register(r"question-group", QuestionGroupViewSet, basename="questioin-group")
router.register(r"question-group-feedback", QuestionGroupFeedbackViewSet, basename="question-group-feedback")
router.register(r"answer", AnswerViewSet, basename="answer")

urlpatterns = [
    path("customers/<int:customer_id>/home-energy-report/", CustomerHomeEnergyReportView.as_view(), name="customer-home-energy-report"),
] + router.urls