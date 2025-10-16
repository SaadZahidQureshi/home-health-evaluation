from django.views.generic import RedirectView
from django.urls import path, include
from .views import *
from django.shortcuts import redirect, render


urlpatterns = [

    #admin page
    path("", RedirectView.as_view(url="login-page/")),
    path("login-page/", AdminSigninPageTemplateView.as_view(), name="admin_sign_in_page"),
    path("token/", AdminTokenPageTemplateView.as_view(), name="admin_token_page"),
    path("users/", AdminUsersPageTemplateView.as_view(), name="admin_users_page"),
    path("profile-settings/", AdminProfileSettingsPageTemplateView.as_view(), name="admin_profile_settings_page"),
    # path("page-not-found/", pageNotFoundPageTemplateView.as_view(), name="page_not_found"),
    path("", include("conf.urls")),
]

handler404 = "conf.error_handlers.custom_404_view"
handler500 = "conf.error_handlers.custom_500_view"