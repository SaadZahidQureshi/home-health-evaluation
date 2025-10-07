
from django.urls import path, include
from .views import *


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

    #admin page
    path("admin-sign-in-page/", adminSigninPageTemplateView.as_view(), name="admin_sign_in_page"),
    path("admin-token-page/", adminTokenPageTemplateView.as_view(), name="admin_token_page"),
    path("admin-users-page/", adminUsersPageTemplateView.as_view(), name="admin_users_page"),
    path("admin-profile-settings-page/", adminProfileSettingsPageTemplateView.as_view(), name="admin_profile_settings_page"),

    path("", include("conf.urls")),
]
