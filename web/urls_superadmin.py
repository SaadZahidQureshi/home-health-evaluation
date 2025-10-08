from django.urls import path, include
from .views import *


urlpatterns = [

    #admin page
    path("login-page/", AdminSigninPageTemplateView.as_view(), name="admin_sign_in_page"),
    path("token/", AdminTokenPageTemplateView.as_view(), name="admin_token_page"),
    path("users/", AdminUsersPageTemplateView.as_view(), name="admin_users_page"),
    path("profile-settings/", AdminProfileSettingsPageTemplateView.as_view(), name="admin_profile_settings_page"),

    path("", include("conf.urls")),
]