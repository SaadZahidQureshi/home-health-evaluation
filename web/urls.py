
from django.urls import path
from .views import *


urlpatterns = [
    path("home/", LandingPageTemplateView.as_view(), name="landing_page"),
    path("", LoginPageTemplateView.as_view(), name="login_page"),
    path("register/", RegisterPageTemplateView.as_view(), name="register_page"),
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
]
