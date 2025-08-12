from django.views.generic import TemplateView
from api.core.mixin import LoginRequiredMixin
from api.home.models import *

# Create your views here.
class LandingPageTemplateView(TemplateView):
    template_name = "index.html"

class LoginPageTemplateView(TemplateView):
    template_name = "sign-in.html"

class RegisterPageTemplateView(TemplateView):
    template_name = "sign-up.html"

class KeepItCleanPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "keep-it-clean.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Keep It Clean: Healthy Home Actions"
        context["active_page"] = "keep_it_clean"
        context["principleId"] = Principle.objects.get(key="CLEAN").id
        return context
    
class KeepItCleanItemSelectedPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "keep-it-clean-item-selected.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Keep It Clean: Healthy Home Actions"
        context["active_page"] = "keep_it_clean"
        context["principleId"] = Principle.objects.get(key="CLEAN").id
        context["questionId"] = self.kwargs['pk']
        return context

class KeepItDryPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "keep-it-dry.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Keep It Dry: Healthy Home Actions"
        context["active_page"] = "keep_it_dry"
        context["principleId"] = Principle.objects.get(key="DRY").id
        return context
    
class KeepItDryItemSelectedPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "keep-it-dry-item-selected.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Keep It Dry: Healthy Home Actions"
        context["active_page"] = "keep_it_dry"
        context["principleId"] = Principle.objects.get(key="DRY").id
        return context

class KeepItMaintainedPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "keep-it-maintained.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Keep It Maintained: Healthy Home Actions"
        context["active_page"] = "keep_it_maintained"
        context["principleId"] = Principle.objects.get(key="MANTAINED").id
        return context
    
class KeepItMaintainedItemSelectedPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "keep-it-maintained-item-selected.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Keep It Maintained: Healthy Home Actions"
        context["active_page"] = "keep_it_maintained"
        context["principleId"] = Principle.objects.get(key="MANTAINED").id
        return context

class KeepItSafePageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "keep-it-safe.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Keep It Safe: Healthy Home Actions"
        context["active_page"] = "keep_it_safe"
        context["principleId"] = Principle.objects.get(key="SAFE").id
        return context

class KeepItPestFreePageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "keep-it-pest-free.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Keep It Pest Free: Healthy Home Actions"
        context["active_page"] = "keep_it_pest_free"
        context["principleId"] = Principle.objects.get(key="PESTFREE").id
        return context

class KeepItPestFreeItemSelectedPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "keep-it-pest-free-item-selected.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Keep It Pest Free: Healthy Home Actions"
        context["active_page"] = "keep_it_pest_free"
        context["principleId"] = Principle.objects.get(key="PESTFREE").id
        return context    

class KeepItCleanContaminentFreePageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "keep-it-clean-contaminent-free.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Keep It Contaminent-Free: Healthy Home Actions"
        context["active_page"] = "keep_it_contaminent_free"
        context["principleId"] = Principle.objects.get(key="CONTAMINANTFREE").id
        return context

class KeepItCleanContaminentFreeItemSelectedPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "keep-it-clean-contaminent-free-item-selected.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Keep It Contaminent-Free: Healthy Home Actions"
        context["active_page"] = "keep_it_contaminent_free"
        context["principleId"] = Principle.objects.get(key="CONTAMINANTFREE").id
        return context

class KeepItVentilatedPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "keep-it-ventilated.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Keep It Ventilated: Healthy Home Actions"
        context["active_page"] = "keep_it_ventilated"
        context["principleId"] = Principle.objects.get(key="VENTILATED").id
        return context

class KeepItVentilatedItemSelectedPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "keep-it-ventilated-item-selected.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Keep It Ventilated: Healthy Home Actions"
        context["active_page"] = "keep_it_ventilated"
        context["principleId"] = Principle.objects.get(key="VENTILATED").id
        return context    

class KeepItComfortablePageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "keep-it-comfortable.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Keep It Comfortable: Healthy Home Actions"
        context["active_page"] = "keep_it_confortable"
        context["principleId"] = Principle.objects.get(key="COMFORTABLE").id
        return context

class KeepItComfortableItemSelectedPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "keep-it-comfortable-item-selected.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Keep It Comfortable: Healthy Home Actions"
        context["active_page"] = "keep_it_confortable"
        context["principleId"] = Principle.objects.get(key="COMFORTABLE").id
        return context

class ProfileSettingPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "profile-settings.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Profile Settings"
        return context
    
class SettingPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "settings.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Settings"
        return context

class SavedgPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "saved.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "Saved"
        context["customerId"] = self.kwargs['pk']
        return context

class HistoryPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "history.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = "History"
        return context
    
class PrincipleDetailsPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "principle-details.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        principle = Principle.objects.get(id=self.kwargs['pk'])
        context["title"] = principle.name
        context["principleId"] = principle.id
        return context
    