from django.views.generic import TemplateView
from api.core.mixin import LoginRequiredMixin
from api.home.models import *
from api.home_energy.models import Step
from django.conf import settings

# Create your views here.
class LandingPageTemplateView(TemplateView):
    template_name = "index.html"

class LoginPageTemplateView(TemplateView):
    template_name = "sign-in.html"

class RegisterPageTemplateView(TemplateView):
    template_name = "sign-up.html"

class AdminSigninPageTemplateView(TemplateView):
    template_name = "admin/admin-sign-in.html"

class AdminTokenPageTemplateView(TemplateView):
    template_name = "admin/admin-token-page.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_admin_sidebar"] = "token"
        return context

class AdminUsersPageTemplateView(TemplateView):
    template_name = "admin/admin-user-page.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_admin_sidebar"] = "users"
        return context
    
class AdminProfileSettingsPageTemplateView(TemplateView):
    template_name = "admin/admin-profile-settings.html"
    

class SideSelectionPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "side-selection.html"

class KeepItCleanPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "keep-it-clean.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Keep It Clean: Healthy Home Actions"
        context["active_page"] = "keep_it_clean"
        context["principleId"] = Principle.objects.get(order=1).id
        return context
    
class KeepItCleanItemSelectedPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "keep-it-clean-item-selected.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Keep It Clean: Healthy Home Actions"
        context["active_page"] = "keep_it_clean"
        context["principleId"] = Principle.objects.get(order=1).id
        context["questionId"] = self.kwargs['pk']
        return context

class KeepItDryPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "keep-it-dry.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Keep It Dry: Healthy Home Actions"
        context["active_page"] = "keep_it_dry"
        context["principleId"] = Principle.objects.get(order=2).id
        return context
    
class KeepItDryItemSelectedPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "keep-it-dry-item-selected.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Keep It Dry: Healthy Home Actions"
        context["active_page"] = "keep_it_dry"
        context["principleId"] = Principle.objects.get(order=2).id
        return context

class KeepItMaintainedPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "keep-it-maintained.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Keep It Maintained: Healthy Home Actions"
        context["active_page"] = "keep_it_maintained"
        context["principleId"] = Principle.objects.get(order=8).id
        return context
    
class KeepItMaintainedItemSelectedPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "keep-it-maintained-item-selected.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Keep It Maintained: Healthy Home Actions"
        context["active_page"] = "keep_it_maintained"
        context["principleId"] = Principle.objects.get(order=8).id
        return context

class KeepItSafePageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "keep-it-safe.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Keep It Safe: Healthy Home Actions"
        context["active_page"] = "keep_it_safe"
        context["principleId"] = Principle.objects.get(order=5).id
        return context

class KeepItPestFreePageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "keep-it-pest-free.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Keep It Pest Free: Healthy Home Actions"
        context["active_page"] = "keep_it_pest_free"
        context["principleId"] = Principle.objects.get(order=3).id
        return context

class KeepItPestFreeItemSelectedPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "keep-it-pest-free-item-selected.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Keep It Pest Free: Healthy Home Actions"
        context["active_page"] = "keep_it_pest_free"
        context["principleId"] = Principle.objects.get(order=3).id
        return context    

class KeepItCleanContaminentFreePageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "keep-it-clean-contaminent-free.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Keep It Contaminent-Free: Healthy Home Actions"
        context["active_page"] = "keep_it_contaminent_free"
        context["principleId"] = Principle.objects.get(order=4).id
        return context

class KeepItCleanContaminentFreeItemSelectedPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "keep-it-clean-contaminent-free-item-selected.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Keep It Contaminent-Free: Healthy Home Actions"
        context["active_page"] = "keep_it_contaminent_free"
        context["principleId"] = Principle.objects.get(order=4).id
        return context

class KeepItVentilatedPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "keep-it-ventilated.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Keep It Ventilated: Healthy Home Actions"
        context["active_page"] = "keep_it_ventilated"
        context["principleId"] = Principle.objects.get(order=6).id
        return context

class KeepItVentilatedItemSelectedPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "keep-it-ventilated-item-selected.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Keep It Ventilated: Healthy Home Actions"
        context["active_page"] = "keep_it_ventilated"
        context["principleId"] = Principle.objects.get(order=6).id
        return context    

class KeepItComfortablePageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "keep-it-comfortable.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Keep It Comfortable: Healthy Home Actions"
        context["active_page"] = "keep_it_confortable"
        context["principleId"] = Principle.objects.get(order=7).id
        return context

class KeepItComfortableItemSelectedPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "keep-it-comfortable-item-selected.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Keep It Comfortable: Healthy Home Actions"
        context["active_page"] = "keep_it_confortable"
        context["principleId"] = Principle.objects.get(order=7).id
        return context

class ProfileSettingPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "profile-settings.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Profile Settings"
        return context
    
class SettingPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "settings.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Settings"
        return context

class SavedgPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "saved.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Saved"
        context["customerId"] = self.kwargs['pk']
        return context

class HistoryPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "History"
        return context
    
class PrincipleDetailsPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "principle-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        principle = Principle.objects.get(id=self.kwargs['pk'])
        context["title"] = principle.name
        context["principleId"] = principle.id
        return context

class FinalRecommendationPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "final-remarks.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["principleId"] = Principle.objects.get(order=9).id
        context["title"] = "Final Recommendations"
        context["active_page"] = "final_remarks"
        return context
    

# Home Energy Side templates

class ExteriorEvaluationFuelLeakTestingPageTemplateView(TemplateView):
    template_name = "home_energy_templates/exterior-evaluation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["principleId"] = Step.objects.get(order=1).id
        context["title"] = "Exterior Evaluation & Fuel Leak Testing"
        context["active_page"] = "exterior_evaluation"
        return context


class InteriorSafetyEvaluationPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "home_energy_templates/interior-safety-evaluation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Interior Safety Evaluation"
        context["principleId"] = Step.objects.get(order=2).id
        context["active_page"] = "interior_safety_evaluation"
        return context


class DoorsWindowsPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "home_energy_templates/doors-windows.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Doors & Windows"
        context["principleId"] = Step.objects.get(order=3).id
        context["active_page"] = "doors_windows"
        return context


class BuildingComponentsConstructionPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "home_energy_templates/building-components-construction.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Building Components & Construction"
        context["principleId"] = Step.objects.get(order=4).id
        context["active_page"] = "building_components_construction"
        return context


class AirflowVentilationPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "home_energy_templates/airflow-ventilation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Airflow & Ventilation"
        context["principleId"] = Step.objects.get(order=5).id
        context["active_page"] = "airflow_ventilation"
        return context


class HVACCombustionSafetyTestingPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "home_energy_templates/hvac-combustion-safety-testing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "HVAC & Combustion Safety Testing"
        context["principleId"] = Step.objects.get(order=6).id
        context["active_page"] = "hvac_combustion_safety"
        return context


class BlowerDoorTestingPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "home_energy_templates/blower-door-testing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Blower Door Testing"
        context["principleId"] = Step.objects.get(order=7).id
        context["active_page"] = "blower_door_testing"
        return context


class AppliancesLightingPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "home_energy_templates/appliances-lighting.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Appliances and Lighting"
        context["principleId"] = Step.objects.get(order=8).id
        context["active_page"] = "appliances_lighting"
        return context


class BaseloadEnergyConsumptionPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "home_energy_templates/baseload-energy-consumption.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Baseload Energy Consumption"
        context["principleId"] = Step.objects.get(order=9).id
        context["active_page"] = "baseload_enery_consumption"
        return context


class FinalRemarksPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "home_energy_templates/final-remarks.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Final Recommendations"
        context["principleId"] = Step.objects.get(order=10).id
        context["active_page"] = "final_remarks"
        return context
    
class HomeEnergyHistoryPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "home_energy_templates/history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "History"
        return context

class HomeEnergySavedPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "home_energy_templates/saved.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Saved"
        context["customerId"] = self.kwargs['pk']
        return context

class StepDetailsPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "home_energy_templates/principle-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        principle = Step.objects.get(id=self.kwargs['pk'])
        context["title"] = principle.title
        context["principleId"] = principle.id
        return context


class HomeEnergyProfileSettingPageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "home_energy_templates/profile-settings.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Profile Settings"
        return context
    

class HomePageTemplateView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "home"
        context["google_map_api"] = settings.GOOGLE_MAP_API
        return context

class PricingPageTemplateView(TemplateView):
    template_name = "home/pricing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "pricing"
        return context

class TermOfServicesTemplateView(TemplateView):
    template_name = "home/term-of-services.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "home"
        return context

class PrivacyPolicyTemplateView(TemplateView):
    template_name = "home/privacy-policy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "home"
        return context
    
class AboutUsPageTemplateView(TemplateView):
    template_name = "home/about-us.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "about_us"
        return context

class ServicesEvaluationPageTemplateView(TemplateView):
    template_name = "home/services-evaluations.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "services"
        return context

class ServicesEnergyAuditPageTemplateView(TemplateView):
    template_name = "home/services-energy-audit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "services"
        return context
    
class BookAppointmentPageTemplateView(TemplateView):
    template_name = "home/book-appointments.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "book_appointments"
        return context
    
class AppointmentDetailsPageTemplateView(TemplateView):
    template_name = "home/appointment-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "book_appointments"
        return context