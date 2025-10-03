from django.urls import path
from rest_framework import routers
from api.administration.views import AdminViewSet
from api.appointments.views import *
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

router.register(r'availability', AvailabilityViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'booking-person', BookingPersonViewSet)

# router.register(r'admin', AdminViewSet, basename="admin")

urlpatterns = [
    path("customers/<int:customer_id>/home-energy-report/", CustomerHomeEnergyReportView.as_view(), name="customer-home-energy-report"),
    path("contact-us/", ContactUsView.as_view(), name="contact-us"),
] + router.urls