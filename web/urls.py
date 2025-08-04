
from django.urls import path
from .views import *


urlpatterns = [
    path("", LandingPageTemplateView.as_view(), name="landing_page"),
    path("login/", LoginPageTemplateView.as_view(), name="login_page"),
    path("register/", RegisterPageTemplateView.as_view(), name="register_page"),
    path("keep-it-clean/", KeepItCleanPageTemplateView.as_view(), name="keep_it_clean_page"),
    path("profile-settings/", ProfileSettingPageTemplateView.as_view(), name="profile_settings_page"),
]
