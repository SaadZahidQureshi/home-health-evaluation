
from django.urls import path, include
from .views import *
from django.shortcuts import redirect


urlpatterns = [
    # home page urls

    path("", HomePageTemplateView.as_view(), name="home_page"),
    path("about-us/", AboutUsPageTemplateView.as_view(), name="about_us_page"),
    path("services-evaluation/", ServicesEvaluationPageTemplateView.as_view(), name="services_evaluation_page"),
    path("services-energy-audit/", ServicesEnergyAuditPageTemplateView.as_view(), name="services_energy_audit_page"),
    path("book-appointments/", BookAppointmentPageTemplateView.as_view(), name="book_appointments_page"),
    path("appointment-details/", AppointmentDetailsPageTemplateView.as_view(), name="appointment_details_page"),
    path("pricing/", PricingPageTemplateView.as_view(), name="pricing_page"),
    path("term-of-services/", TermOfServicesTemplateView.as_view(), name="term_of_services_page"),
    path("privacy-policy/", PrivacyPolicyTemplateView.as_view(), name="privacy_policy_page"),
    # path("page-not-found/", pageNotFoundPageTemplateView.as_view(), name="page_not_found"),

    path("", include("conf.urls")),
]

handler404 = "conf.error_handlers.custom_404_view"
handler500 = "conf.error_handlers.custom_500_view"