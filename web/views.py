from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class LandingPageTemplateView(TemplateView):
    template_name = "index.html"

class LoginPageTemplateView(TemplateView):
    template_name = "sign-in.html"

class RegisterPageTemplateView(TemplateView):
    template_name = "sign-up.html"

class KeepItCleanPageTemplateView(TemplateView):
    template_name = "keep-it-clean.html"

class ProfileSettingPageTemplateView(TemplateView):
    template_name = "profile-settings.html"