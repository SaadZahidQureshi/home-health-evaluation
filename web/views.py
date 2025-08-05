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

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Keep It Clean: Healthy Home Actions"
        context["active_page"] = "keep_it_clean"
        return context
    
class KeepItCleanItemSelectedPageTemplateView(TemplateView):
    template_name = "keep-it-clean-item-selected.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Keep It Clean: Healthy Home Actions"
        context["active_page"] = "keep_it_clean"
        return context

class KeepItDryPageTemplateView(TemplateView):
    template_name = "keep-it-dry.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Keep It Dry: Healthy Home Actions"
        context["active_page"] = "keep_it_dry"
        return context
    
class KeepItDryItemSelectedPageTemplateView(TemplateView):
    template_name = "keep-it-dry-item-selected.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Keep It Dry: Healthy Home Actions"
        context["active_page"] = "keep_it_dry"
        return context

class KeepItMaintainedPageTemplateView(TemplateView):
    template_name = "keep-it-maintained.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Keep It Maintained: Healthy Home Actions"
        context["active_page"] = "keep_it_maintained"
        return context
    
class KeepItMaintainedItemSelectedPageTemplateView(TemplateView):
    template_name = "keep-it-maintained-item-selected.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Keep It Maintained: Healthy Home Actions"
        context["active_page"] = "keep_it_maintained"
        return context

class KeepItSafePageTemplateView(TemplateView):
    template_name = "keep-it-safe.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Keep It Safe: Healthy Home Actions"
        context["active_page"] = "keep_it_safe"
        return context

class KeepItPestFreePageTemplateView(TemplateView):
    template_name = "keep-it-pest-free.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Keep It Pest Free: Healthy Home Actions"
        context["active_page"] = "keep_it_pest_free"
        return context

class KeepItPestFreeItemSelectedPageTemplateView(TemplateView):
    template_name = "keep-it-pest-free-item-selected.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Keep It Pest Free: Healthy Home Actions"
        context["active_page"] = "keep_it_pest_free"
        return context    

class KeepItCleanContaminentFreePageTemplateView(TemplateView):
    template_name = "keep-it-clean-contaminent-free.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Keep It Contaminent-Free: Healthy Home Actions"
        context["active_page"] = "keep_it_contaminent_free"
        return context

class KeepItCleanContaminentFreeItemSelectedPageTemplateView(TemplateView):
    template_name = "keep-it-clean-contaminent-free-item-selected.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Keep It Contaminent-Free: Healthy Home Actions"
        context["active_page"] = "keep_it_contaminent_free"
        return context

class KeepItVentilatedPageTemplateView(TemplateView):
    template_name = "keep-it-ventilated.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Keep It Ventilated: Healthy Home Actions"
        context["active_page"] = "keep_it_ventilated"
        return context

class KeepItVentilatedItemSelectedPageTemplateView(TemplateView):
    template_name = "keep-it-ventilated-item-selected.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Keep It Ventilated: Healthy Home Actions"
        context["active_page"] = "keep_it_ventilated"
        return context    

class KeepItComfortablePageTemplateView(TemplateView):
    template_name = "keep-it-comfortable.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Keep It Comfortable: Healthy Home Actions"
        context["active_page"] = "keep_it_confortable"
        return context

class KeepItComfortableItemSelectedPageTemplateView(TemplateView):
    template_name = "keep-it-comfortable-item-selected.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Keep It Comfortable: Healthy Home Actions"
        context["active_page"] = "keep_it_confortable"
        return context

class ProfileSettingPageTemplateView(TemplateView):
    template_name = "profile-settings.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Profile Settings"
        return context
    
class SettingPageTemplateView(TemplateView):
    template_name = "settings.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Settings"
        return context

class SavedgPageTemplateView(TemplateView):
    template_name = "saved.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Saved"
        return context

class HistoryPageTemplateView(TemplateView):
    template_name = "history.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "History"
        return context