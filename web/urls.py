
from django.urls import path
from .views import *


urlpatterns = [
    path("home/", LandingPageTemplateView.as_view(), name="landing_page"),
    path("", LoginPageTemplateView.as_view(), name="login_page"),
    path("register/", RegisterPageTemplateView.as_view(), name="register_page"),
    path("side-selection/", SideSelectionPageTemplateView.as_view(), name="side_selection"),
    path("settings/", SettingPageTemplateView.as_view(), name="settings_page"),
    path("profile-settings/", ProfileSettingPageTemplateView.as_view(), name="profile_settings_page"),
    path("saved/<int:pk>", SavedgPageTemplateView.as_view(), name="saved_page"),
    path("history/", HistoryPageTemplateView.as_view(), name="history_page"),
    path("keep-it-clean/", KeepItCleanPageTemplateView.as_view(), name="keep_it_clean_page"),
    path("keep-it-clean-item-selected/<int:pk>/", KeepItCleanItemSelectedPageTemplateView.as_view(), name="keep_it_clean_item_selected_page"),
    path("keep-it-dry/", KeepItDryPageTemplateView.as_view(), name="keep_it_dry_page"),
    path("keep-it-dry-item-selected/", KeepItDryItemSelectedPageTemplateView.as_view(), name="keep_it_dry_item_selected_page"),
    path("keep-it-safe/", KeepItSafePageTemplateView.as_view(), name="keep_it_safe_page"),
    path("keep-it-pest-free/", KeepItPestFreePageTemplateView.as_view(), name="keep_it_pest_free_page"),
    path("keep-it-pest-free-item-selected/", KeepItPestFreeItemSelectedPageTemplateView.as_view(), name="keep_it_pest_free_item_selected_page"),
    path("keep-it-maintained/", KeepItMaintainedPageTemplateView.as_view(), name="keep_it_maintained_page"),
    path("keep-it-maintained-item-selected/", KeepItMaintainedItemSelectedPageTemplateView.as_view(), name="keep_it_maintained_item_selected_page"),
    path("keep-it-ventilated/", KeepItVentilatedPageTemplateView.as_view(), name="keep_it_ventilated_page"),
    path("keep-it-ventilated-item-selected/", KeepItVentilatedItemSelectedPageTemplateView.as_view(), name="keep_it_ventilated_item_selected_page"),
    path("keep-it-comfortable/", KeepItComfortablePageTemplateView.as_view(), name="keep_it_comfortable_page"),
    path("keep-it-comfortable-item-selected/", KeepItComfortableItemSelectedPageTemplateView.as_view(), name="keep_it_comfortable_item_selected_page"),
    path("keep-it-clean-contaminent-free/", KeepItCleanContaminentFreePageTemplateView.as_view(), name="keep_it_clean_contaminent_free_page"),
    path("keep-it-clean-contaminent-free-item-selected/", KeepItCleanContaminentFreeItemSelectedPageTemplateView.as_view(), name="keep_it_clean_contaminent_free_item_selected_page"),
    path("principle/details/<int:pk>", PrincipleDetailsPageTemplateView.as_view(), name="principle_detail_page"),
    path("final-recommendations/", FinalRecommendationPageTemplateView.as_view(), name="final_recommendations_page"),
    path("pdf-report/", PDFTemplatePageTemplateView.as_view(), name="pdf_report"),


    # Home Energy Side URLs
    
    path("exterior-evaluation/", ExteriorEvaluationFuelLeakTestingPageTemplateView.as_view(), name="exterior_evaluation"),
    path("interior-safety-evaluation/", InteriorSafetyEvaluationPageTemplateView.as_view(), name="interior_safety_evaluation"),
    path("doors-windows/", DoorsWindowsPageTemplateView.as_view(), name="doors_windows"),
    path("building-components/", BuildingComponentsConstructionPageTemplateView.as_view(), name="building_components"),
    path("airflow-ventilation/", AirflowVentilationPageTemplateView.as_view(), name="airflow_ventilation"),
    path("hvac-combustion-safety-testing/", HVACCombustionSafetyTestingPageTemplateView.as_view(), name="hvac_combustion_safety_testing"),
    path("blower-door-testing/", BlowerDoorTestingPageTemplateView.as_view(), name="blower_door_testing"),
    path("appliances-lighting/", AppliancesLightingPageTemplateView.as_view(), name="appliances_lighting"),
    path("baseload-energy-consumption/", BaseloadEnergyConsumptionPageTemplateView.as_view(), name="baseload_energy_consumption"),
    path("home-energy/final-remarks/", FinalRemarksPageTemplateView.as_view(), name="final_remarks"),
    path("home-energy/history/", HomeEnergyHistoryPageTemplateView.as_view(), name="home_energy_history"),
    path("home-energy/saved/<int:pk>", HomeEnergySavedPageTemplateView.as_view(), name="home_energy_saved"),
    path("step/details/<int:pk>", StepDetailsPageTemplateView.as_view(), name="step_detail_page"),
    path("home-energy/profile-settings/", HomeEnergyProfileSettingPageTemplateView.as_view(), name="home_energy_profile_settings_page"),
]
