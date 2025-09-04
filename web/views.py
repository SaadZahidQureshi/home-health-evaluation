from django.views.generic import TemplateView
from api.core.mixin import LoginRequiredMixin
from api.home.models import *
from api.home_energy.models import Step

# Create your views here.
class LandingPageTemplateView(TemplateView):
    template_name = "index.html"

class LoginPageTemplateView(TemplateView):
    template_name = "sign-in.html"

class RegisterPageTemplateView(TemplateView):
    template_name = "sign-up.html"

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
    

class PDFTemplatePageTemplateView(TemplateView):
    template_name = "email/healthy_home_report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["principleId"] = Principle.objects.get(order=9).id
        context["title"] = "Final Recommendations"
        context["active_page"] = "final_remarks"
        context["data"] = {
                                "customer": {
                                "name": "saad",
                                "email": "dev.saadzahidqureshi+test@gmail.com",
                                "house_image": "/media/house_images/Screenshot_2025-08-23_at_1.08.21_am-removebg-preview.png",
                                "address": "test",
                                "city": "TEST CITY",
                                "state": "test",
                                "zip": "123234"
                                },
                                "principles": [
                                {
                                    "principle": {
                                    "id": 1,
                                    "created_at": "2023-01-01T00:00:00+00:00",
                                    "updated_at": "2023-01-01T00:00:00+00:00",
                                    "name": "Keep It Clean",
                                    "order": 1,
                                    "key": "CLEAN"
                                    },
                                    "categories": [
                                    {
                                        "id": 1,
                                        "name": "Building",
                                        "order": 1,
                                        "is_answered": False,
                                        "feedback": {
                                        "id": 5,
                                        "note": "Earum perferendis nu",
                                        "images": [
                                            {
                                            "id": 62,
                                            "created_at": "2025-09-02T06:28:05.808008+00:00",
                                            "updated_at": "2025-09-02T06:28:05.808008+00:00",
                                            "image": "/media/answer_photos/new_test_qr_code_yDH7cEr.PNG"
                                            },
                                            {
                                            "id": 63,
                                            "created_at": "2025-09-02T06:28:05.848995+00:00",
                                            "updated_at": "2025-09-02T06:28:05.848995+00:00",
                                            "image": "/media/answer_photos/test_qr_code_4yHkUMq.PNG"
                                            },
                                            {
                                            "id": 64,
                                            "created_at": "2025-09-02T06:28:05.878140+00:00",
                                            "updated_at": "2025-09-02T06:28:05.878140+00:00",
                                            "image": "/media/answer_photos/screencapture-uoneroof-contact-2025-08-21-16_38_02_1NV90bV.png"
                                            }
                                        ]
                                        },
                                        "options": [
                                        {
                                            "id": 1,
                                            "text": "Have hard surfaces outside the home at entry doors",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 2,
                                            "text": "Have a space to leave shoes by the door",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 3,
                                            "text": "Use pollen-filtering screens on windows",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 4,
                                            "text": "Have hard-surface floors inside the home, if possible",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 5,
                                            "text": "Use low-pile carpet if hard-surface floors are not an option",
                                            "is_selected": False
                                        }
                                        ],
                                        "subcategories": [],
                                        "applicable": False
                                    },
                                    {
                                        "id": 2,
                                        "name": "Mechanical",
                                        "order": 2,
                                        "is_answered": False,
                                        "feedback": {
                                        "id": 6,
                                        "note": "Facere praesentium e",
                                        "images": []
                                        },
                                        "options": [
                                        {
                                            "id": 6,
                                            "text": "Ensure the duct system is free of dust, mold, and pests",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 7,
                                            "text": "For those with allergies and asthma, consider upgrading to a furnace filter with a minimum efficiency value (MERV) of 11-13 in HVAC systems, and replace it on the recommended schedule. (Be sure to check with your HVAC service company to make sure your system can handle the higher efficiency filter.)",
                                            "is_selected": False
                                        }
                                        ],
                                        "subcategories": [],
                                        "applicable": False
                                    },
                                    {
                                        "id": 3,
                                        "name": "Environment",
                                        "order": 3,
                                        "is_answered": False,
                                        "feedback": {
                                        "id": 7,
                                        "note": "Dolor dicta voluptat",
                                        "images": []
                                        },
                                        "options": [
                                        {
                                            "id": 8,
                                            "text": "Keep the outdoors outside the home",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 9,
                                            "text": "Close windows on high smog and high pollen days and when pesticides or other chemicals are being used.",
                                            "is_selected": False
                                        }
                                        ],
                                        "subcategories": [],
                                        "applicable": False
                                    },
                                    {
                                        "id": 4,
                                        "name": "Occupants",
                                        "order": 4,
                                        "is_answered": False,
                                        "feedback": {
                                        "id": 8,
                                        "note": "Voluptatum excepturi",
                                        "images": []
                                        },
                                        "options": [
                                        {
                                            "id": 10,
                                            "text": "Clear clutter from the home.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 11,
                                            "text": "Keep dust-producing activities outside (e.g., cutting wood for home projects).",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 12,
                                            "text": "Use a vacuum cleaner equipped with an allergen-capturing bag and a HEPA-filtered exhaust to prevent allergens from being redistributed.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 13,
                                            "text": "Wet-dust using a damp cloth or sponge. Dry-dusting moves the dust around but doesn't completely collect it.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 14,
                                            "text": "Use a washable pad or microfiber pad to wet-clean floors.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 15,
                                            "text": "Take shoes off at the door.",
                                            "is_selected": False
                                        }
                                        ],
                                        "subcategories": [],
                                        "applicable": False
                                    }
                                    ]
                                },
                                {
                                    "principle": {
                                    "id": 2,
                                    "created_at": "2023-01-01T00:00:00+00:00",
                                    "updated_at": "2023-01-01T00:00:00+00:00",
                                    "name": "Keep It Dry",
                                    "order": 2,
                                    "key": "DRY"
                                    },
                                    "categories": [
                                    {
                                        "id": 5,
                                        "name": "Building",
                                        "order": 5,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [
                                        {
                                            "id": 16,
                                            "text": "Ensure gutters are working and downspouts direct water away from the foundation.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 17,
                                            "text": "Grade dirt away from the house.  It should be lower away from the foundation than it is next to it.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 18,
                                            "text": "Repair leaks (roof, doors, windows, plumbing).",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 19,
                                            "text": "Repair foundation cracks.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 20,
                                            "text": "Install storm windows to help prevent condensation.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 21,
                                            "text": "Control moisture in a crawl space with a properly-installed ground cover.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 22,
                                            "text": "Be wary of passive ventilation in a basement or crawl space.",
                                            "is_selected": False
                                        }
                                        ],
                                        "subcategories": [],
                                        "applicable": True
                                    },
                                    {
                                        "id": 6,
                                        "name": "Mechanical",
                                        "order": 6,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [
                                        {
                                            "id": 23,
                                            "text": "Ensure bathrooms have fans vented to the outside.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 24,
                                            "text": "Ensure the kitchen has a fan vented to the outside.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 25,
                                            "text": "Ensure the clothes dryer is vented to the outside.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 26,
                                            "text": "Consider a whole-house dehumidifier.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 27,
                                            "text": "Use the bathroom fan when bathing.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 28,
                                            "text": "Use the kitchen fan when cooking.",
                                            "is_selected": False
                                        }
                                        ],
                                        "subcategories": [],
                                        "applicable": True
                                    },
                                    {
                                        "id": 7,
                                        "name": "Occupants",
                                        "order": 7,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [
                                        {
                                            "id": 29,
                                            "text": "Keep the dryer vent clear of lint and ensure that it is properly vented to the outdoors.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 30,
                                            "text": "Use a portable dehumidifier in the basement or crawlspace. Empty and clean it regularly.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 31,
                                            "text": "Dry spills immediately.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 32,
                                            "text": "Be mindful of having too many houseplants, fish tanks, and other sources of standing water.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 33,
                                            "text": "Throw away wet material.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 34,
                                            "text": "Promote airflow. Doors can be undercut by an inch, closet doors can be left cracked, and furniture can be moved a few inches away from walls.",
                                            "is_selected": False
                                        }
                                        ],
                                        "subcategories": [],
                                        "applicable": True
                                    }
                                    ]
                                },
                                {
                                    "principle": {
                                    "id": 3,
                                    "created_at": "2023-01-01T00:00:00+00:00",
                                    "updated_at": "2023-01-01T00:00:00+00:00",
                                    "name": "Keep It Pest-Free",
                                    "order": 3,
                                    "key": "PESTFREE"
                                    },
                                    "categories": [
                                    {
                                        "id": 8,
                                        "name": "Environment",
                                        "order": 8,
                                        "is_answered": True,
                                        "feedback": {
                                        "id": 9,
                                        "note": "testing",
                                        "images": [
                                            {
                                            "id": 66,
                                            "created_at": "2025-09-04T06:22:17.817838+00:00",
                                            "updated_at": "2025-09-04T06:22:17.817918+00:00",
                                            "image": "/media/answer_photos/Interior_Safety_Evaluation_oLmLjn8.png"
                                            },
                                            {
                                            "id": 67,
                                            "created_at": "2025-09-04T06:22:17.832322+00:00",
                                            "updated_at": "2025-09-04T06:22:17.832322+00:00",
                                            "image": "/media/answer_photos/Exterior_Evaluation_dlKpLny.png"
                                            }
                                        ]
                                        },
                                        "options": [],
                                        "subcategories": [
                                        {
                                            "id": 9,
                                            "name": "Rodents",
                                            "order": 9,
                                            "is_answered": True,
                                            "feedback": None,
                                            "options": [
                                            {
                                                "id": 35,
                                                "text": "Don’t store firewood indoors or in a garage",
                                                "is_selected": True
                                            },
                                            {
                                                "id": 36,
                                                "text": "Remove garbage from the outdoor environment",
                                                "is_selected": True
                                            },
                                            {
                                                "id": 37,
                                                "text": "Keep firewood and scrap lumber at least 20 ft. from the house;  keep it 18 inches off the ground to prevent nesting.",
                                                "is_selected": True
                                            },
                                            {
                                                "id": 38,
                                                "text": "Eliminate food and water sources from the indoor environment.",
                                                "is_selected": False
                                            }
                                            ],
                                            "subcategories": [],
                                            "applicable": True
                                        },
                                        {
                                            "id": 10,
                                            "name": "Cockroaches",
                                            "order": 10,
                                            "is_answered": True,
                                            "feedback": None,
                                            "options": [
                                            {
                                                "id": 39,
                                                "text": "Inspect items brought into the home (grocery bags, pet food, boxes of food or beverages).",
                                                "is_selected": True
                                            },
                                            {
                                                "id": 40,
                                                "text": "Eliminate food and water sources from the indoor environment",
                                                "is_selected": True
                                            },
                                            {
                                                "id": 41,
                                                "text": "Place bait traps or gels in the indoor environment",
                                                "is_selected": True
                                            }
                                            ],
                                            "subcategories": [],
                                            "applicable": True
                                        },
                                        {
                                            "id": 11,
                                            "name": "Dust Mites",
                                            "order": 11,
                                            "is_answered": True,
                                            "feedback": None,
                                            "options": [
                                            {
                                                "id": 42,
                                                "text": "Keep RH (Relative Humidity) below 50%, which will lead to dust mites drying out (dehydrating)",
                                                "is_selected": True
                                            }
                                            ],
                                            "subcategories": [],
                                            "applicable": True
                                        }
                                        ],
                                        "applicable": True
                                    },
                                    {
                                        "id": 12,
                                        "name": "Building",
                                        "order": 12,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [],
                                        "subcategories": [
                                        {
                                            "id": 14,
                                            "name": "Rodents",
                                            "order": 14,
                                            "is_answered": False,
                                            "feedback": None,
                                            "options": [
                                            {
                                                "id": 43,
                                                "text": "Add door sweeps to all entry doors.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 44,
                                                "text": "Seal all cracks with silicone caulk.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 45,
                                                "text": "Identify any openings larger than ¼ inch.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 46,
                                                "text": "Fill small openings with stainless steel or copper mesh; seal with silicone caulk.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 47,
                                                "text": "Seal large openings with material rodents cannot chew through, such as concrete or sheet metal.",
                                                "is_selected": False
                                            }
                                            ],
                                            "subcategories": [],
                                            "applicable": False
                                        },
                                        {
                                            "id": 15,
                                            "name": "Cockroaches",
                                            "order": 15,
                                            "is_answered": False,
                                            "feedback": None,
                                            "options": [
                                            {
                                                "id": 48,
                                                "text": "Seal all cracks with silicone caulk.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 49,
                                                "text": "Use weatherstripping to fill gaps around windows and doors.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 50,
                                                "text": "Repair all exterior leaks.",
                                                "is_selected": False
                                            }
                                            ],
                                            "subcategories": [],
                                            "applicable": False
                                        },
                                        {
                                            "id": 16,
                                            "name": "Dust Mites",
                                            "order": 16,
                                            "is_answered": False,
                                            "feedback": None,
                                            "options": [
                                            {
                                                "id": 51,
                                                "text": "Seal exterior leaks to reduce excess moisture.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 52,
                                                "text": "Have hard-surface floors inside the home, if possible.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 53,
                                                "text": "Use low-pile carpet if hard-surface floors are not an option.",
                                                "is_selected": False
                                            }
                                            ],
                                            "subcategories": [],
                                            "applicable": False
                                        },
                                        {
                                            "id": 17,
                                            "name": "Bed Bugs",
                                            "order": 17,
                                            "is_answered": False,
                                            "feedback": None,
                                            "options": [
                                            {
                                                "id": 54,
                                                "text": "Seal interior openings around plumbing or electrical wiring to limit bed bugs ability to migrate to other nesting areas.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 55,
                                                "text": "Seal around crown molding and baseboard molding with silicone caulk to limit bed bugs ability to migrate to other nesting areas.",
                                                "is_selected": False
                                            }
                                            ],
                                            "subcategories": [],
                                            "applicable": False
                                        }
                                        ],
                                        "applicable": True
                                    },
                                    {
                                        "id": 18,
                                        "name": "Mechanical",
                                        "order": 18,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [],
                                        "subcategories": [
                                        {
                                            "id": 19,
                                            "name": "Cockroaches",
                                            "order": 19,
                                            "is_answered": False,
                                            "feedback": None,
                                            "options": [
                                            {
                                                "id": 56,
                                                "text": "Repair all interior leaks",
                                                "is_selected": False
                                            }
                                            ],
                                            "subcategories": [],
                                            "applicable": False
                                        },
                                        {
                                            "id": 20,
                                            "name": "Dust Mites",
                                            "order": 20,
                                            "is_answered": False,
                                            "feedback": None,
                                            "options": [
                                            {
                                                "id": 57,
                                                "text": "Repair plumbing leaks to reduce excess moisture.",
                                                "is_selected": False
                                            }
                                            ],
                                            "subcategories": [],
                                            "applicable": False
                                        }
                                        ],
                                        "applicable": True
                                    },
                                    {
                                        "id": 21,
                                        "name": "Occupants",
                                        "order": 21,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [],
                                        "subcategories": [
                                        {
                                            "id": 22,
                                            "name": "Rodents",
                                            "order": 22,
                                            "is_answered": False,
                                            "feedback": None,
                                            "options": [
                                            {
                                                "id": 491,
                                                "text": "Develop and maintain a cleaning schedule.",
                                                "is_selected": False
                                            }
                                            ],
                                            "subcategories": [],
                                            "applicable": False
                                        },
                                        {
                                            "id": 23,
                                            "name": "Cockroaches",
                                            "order": 23,
                                            "is_answered": False,
                                            "feedback": None,
                                            "options": [
                                            {
                                                "id": 58,
                                                "text": "Develop and maintain a cleaning schedule.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 59,
                                                "text": "Establish a monitoring process. In multi-family buildings, a monitoring program involving all of the residents may be necessary.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 60,
                                                "text": "Check clothing, backpacks, and luggage whenever traveling and returning home.",
                                                "is_selected": False
                                            }
                                            ],
                                            "subcategories": [],
                                            "applicable": False
                                        },
                                        {
                                            "id": 24,
                                            "name": "Dust Mites",
                                            "order": 24,
                                            "is_answered": False,
                                            "feedback": None,
                                            "options": [
                                            {
                                                "id": 61,
                                                "text": "Wash bedding and blankets weekly in hot water to kill dust mites.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 62,
                                                "text": "Use dust mite-proof covers to prevent dust mites from nesting in mattresses and pillows and launder them monthly.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 63,
                                                "text": "Avoid cloth window treatments. Alternatively wash them.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 64,
                                                "text": "Wash stuffed animals or put them in the freezer for at least two days.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 65,
                                                "text": "Vacuum all surfaces regularly (carpets, rugs, furniture).",
                                                "is_selected": False
                                            }
                                            ],
                                            "subcategories": [],
                                            "applicable": False
                                        },
                                        {
                                            "id": 25,
                                            "name": "Bed Bugs",
                                            "order": 25,
                                            "is_answered": False,
                                            "feedback": None,
                                            "options": [
                                            {
                                                "id": 66,
                                                "text": "Check clothing, backpacks, and luggage whenever traveling and returning home.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 67,
                                                "text": "Eliminate clutter in which bed bugs can nest; store items in closed bins.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 68,
                                                "text": "Vacuum using a HEPA filter or bag in the vacuum. Double-bag and dispose of the vacuum bag immediately.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 69,
                                                "text": "Seal mattresses in a bed bug-proof cover. Bed bugs will die if they are unable to feed.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 70,
                                                "text": "Wash all bedding in hot water weekly to kill bed bugs.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 71,
                                                "text": "Use interceptors under each bed post.",
                                                "is_selected": False
                                            }
                                            ],
                                            "subcategories": [],
                                            "applicable": False
                                        }
                                        ],
                                        "applicable": True
                                    }
                                    ]
                                },
                                {
                                    "principle": {
                                    "id": 4,
                                    "created_at": "2023-01-01T00:00:00+00:00",
                                    "updated_at": "2023-01-01T00:00:00+00:00",
                                    "name": "Keep It Contaminant-Free",
                                    "order": 4,
                                    "key": "CONTAMINANTFREE"
                                    },
                                    "categories": [
                                    {
                                        "id": 26,
                                        "name": "Building",
                                        "order": 26,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [
                                        {
                                            "id": 72,
                                            "text": "Wash walls and ceilings with soap and water to remove tobacco smoke contaminants.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 73,
                                            "text": "Repaint walls with 2-3 coats of paint to encapsulate nicotine.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 74,
                                            "text": "Remove carpet and padding and wash the floors before replacing carpeting.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 75,
                                            "text": "Choose VOC-free and low-VOC options for paint, floor finishes, carpet, cabinets, and other items that become a permanent or semi-permanent aspect of the home.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 76,
                                            "text": "Avoid paint that uses ethylene glycol.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 77,
                                            "text": "Avoid acid-cured polyurethane finishes for floors.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 78,
                                            "text": "When building or remodeling, use hardwood plywood or particleboard that complies with Toxic Substances Control Act Title VI.",
                                            "is_selected": False
                                        }
                                        ],
                                        "subcategories": [],
                                        "applicable": True
                                    },
                                    {
                                        "id": 27,
                                        "name": "Mechanical",
                                        "order": 27,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [
                                        {
                                            "id": 79,
                                            "text": "Follow ventilation recommendations to keep air truly fresh.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 80,
                                            "text": "Use air conditioning to keep the home at a comfortable temperature. Higher temperatures increase off-gassing.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 81,
                                            "text": "Use dehumidifiers to keep relative humidity between 40-60%. Higher RH increases off-gassing.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 82,
                                            "text": "Replace the furnace filter on a routine basis, somewhere between monthly and quarterly depending on how dusty indoor conditions appear to be.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 83,
                                            "text": "Ensure the home is adequately ventilated, which means bringing in fresh outdoor air and removing stale air.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 84,
                                            "text": "Increase ventilation when products containing VOC’s are used. Use fans to have 2-5 air changes per hour during application and for 48 hours afterwards.",
                                            "is_selected": False
                                        }
                                        ],
                                        "subcategories": [],
                                        "applicable": True
                                    },
                                    {
                                        "id": 28,
                                        "name": "Environment",
                                        "order": 28,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [
                                        {
                                            "id": 85,
                                            "text": "Increase ventilation if formaldehyde contamination is suspected.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 86,
                                            "text": "Avoid using chemical air fresheners and scented products.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 87,
                                            "text": "Clean window treatments to eliminate off-gassing of third-hand smoke.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 88,
                                            "text": "Do not smoke, or at least do not smoke indoors.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 89,
                                            "text": "If renting, ask the property owner or manager about adopting a smoke-free policy.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 90,
                                            "text": "Choose VOC-free or low-VOC products.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 91,
                                            "text": "Avoid terpenes (turpentine and furniture varnish) and linseed oil.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 92,
                                            "text": "Do not idle cars in an attached garage.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 93,
                                            "text": "Use Integrated Pest Management (IPM) to reduce the use of pesticides in the home.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 94,
                                            "text": "Obtain, read, and follow Safety Data Sheets when available.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 95,
                                            "text": "Follow label instructions. Note that a well-ventilated area is either outdoors or a place that has an exhaust fan that meets the recommendations given above in Mechanicals.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 96,
                                            "text": "Store products outside of the living space, if possible (e.g., garage, shed).",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 97,
                                            "text": "If materials must be stored in the home, find a well-ventilated area.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 98,
                                            "text": "Store products out of sight and out of reach. Use child-safe locks or latches to limit access.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 99,
                                            "text": "Buy only what is needed so that extra VOC-containing products don’t need to be stored.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 100,
                                            "text": "Safely dispose of old products that are no longer needed. Instead of throwing them out, find out if the city/town runs a collection program for household waste.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 101,
                                            "text": "When purchasing composite wood products (e.g., flat-pack furniture, children’s play furniture), verify they comply with TSCA Title VI.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 102,
                                            "text": "Choose phthalate-free products.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 103,
                                            "text": "Minimize exposure when working with products that may contain phthalate.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 104,
                                            "text": "Have a track-off system and remove footwear when entering the home.",
                                            "is_selected": False
                                        }
                                        ],
                                        "subcategories": [],
                                        "applicable": True
                                    },
                                    {
                                        "id": 29,
                                        "name": "Occupants",
                                        "order": 29,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [
                                        {
                                            "id": 105,
                                            "text": "Take all unused cleaning, hobby, remodeling and other household products to a local household hazardous waste collection instead of placing in the trash to go to a landfill.",
                                            "is_selected": False
                                        }
                                        ],
                                        "subcategories": [],
                                        "applicable": True
                                    }
                                    ]
                                },
                                {
                                    "principle": {
                                    "id": 5,
                                    "created_at": "2023-01-01T00:00:00+00:00",
                                    "updated_at": "2023-01-01T00:00:00+00:00",
                                    "name": "Keep It Safe",
                                    "order": 5,
                                    "key": "SAFE"
                                    },
                                    "categories": [
                                    {
                                        "id": 30,
                                        "name": "Occupants(Poisoning)",
                                        "order": 30,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [
                                        {
                                            "id": 106,
                                            "text": "Program the number for Poison Control into cell phones and post it near land-line phones: 1-800-222-1222.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 107,
                                            "text": "Read labels when purchasing products and choose products that are less hazardous.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 108,
                                            "text": "Keep products in their original containers, which will have all required hazard warnings.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 109,
                                            "text": "Store cleaning products out of reach and out of sight of children.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 110,
                                            "text": "Use child safety latches/locks on cabinets.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 111,
                                            "text": "Store poisonous items out of reach and out of sight of children. If this is not possible, use child safety latches/locks on cabinets.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 112,
                                            "text": "Store medicine and vitamins out of reach and out of sight. If pill organizers are needed, set alarm reminders instead of leaving the pill organizer out as a visual reminder.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 113,
                                            "text": "Households without children should still consider making their hazardous products “pet-proof.”",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 114,
                                            "text": "Dispose of unused medicines via city or town take-back programs.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 115,
                                            "text": "Keep poisonous plants out of the home.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 116,
                                            "text": "Know which outdoor plants are poisonous and restrict children’s access to them.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 117,
                                            "text": "Purchase only nontoxic arts and crafts supplies for children.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 118,
                                            "text": "Install CO alarms on every floor of the home.",
                                            "is_selected": False
                                        }
                                        ],
                                        "subcategories": [],
                                        "applicable": True
                                    },
                                    {
                                        "id": 31,
                                        "name": "Building(Falls)",
                                        "order": 31,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [
                                        {
                                            "id": 119,
                                            "text": "Ensure stairways meet current code requirements for uniform riser height and tread depth and are properly lit.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 120,
                                            "text": "Install handrails when there are four or more risers in a flight of stairs (or fewer if required by local code).",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 121,
                                            "text": "Depending on occupant needs, install chair-height toilets.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 122,
                                            "text": "Add windows guards to upper-story windows; these protective bars screw into framing studs (not decorative trim) to prevent falls.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 123,
                                            "text": "Use portable gates at opening for exterior stairs to prevent young children from falling.",
                                            "is_selected": False
                                        }
                                        ],
                                        "subcategories": [],
                                        "applicable": True
                                    },
                                    {
                                        "id": 32,
                                        "name": "Environment(Falls)",
                                        "order": 32,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [
                                        {
                                            "id": 124,
                                            "text": "Ensure that exterior and interior lighting is sufficiently bright that occupants and visitors can see where they are walking. Motion sensor lights in hallways and bathrooms are an option.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 125,
                                            "text": "Grade exterior walkways so that water does not pool on them.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 126,
                                            "text": "Use soft materials under children’s play areas.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 127,
                                            "text": "Cap old, unused wells according to local building code.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 128,
                                            "text": "Place nonslip mats or adhesive strips in shower stalls and bathtubs.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 129,
                                            "text": "Place nonslip adhesive strips on stairs.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 130,
                                            "text": "Use safety gates at the top and bottom of stairs inside homes that have young children.",
                                            "is_selected": False
                                        }
                                        ],
                                        "subcategories": [],
                                        "applicable": True
                                    },
                                    {
                                        "id": 33,
                                        "name": "Occupants(falls)",
                                        "order": 33,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [
                                        {
                                            "id": 131,
                                            "text": "Remove clutter from the home.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 132,
                                            "text": "Put away children’s toys and pet toys.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 133,
                                            "text": "Remove area rugs and small furniture.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 134,
                                            "text": "Rearrange furniture to allow for wide walking paths through rooms.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 135,
                                            "text": "Clear snow and ice from exterior stairs and walkways.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 136,
                                            "text": "Properly dispose of old lumber and building materials that present a trip and fall hazard.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 137,
                                            "text": "Remove a trampoline if possible or ensure that existing trampolines have appropriate safety features.",
                                            "is_selected": False
                                        }
                                        ],
                                        "subcategories": [],
                                        "applicable": True
                                    },
                                    {
                                        "id": 34,
                                        "name": "Mechanical(Fires and Burns)",
                                        "order": 34,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [
                                        {
                                            "id": 138,
                                            "text": "Hire a licensed electrician to investigate and repair blown fuses/tripped circuit breakers.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 139,
                                            "text": "Hire a licensed electrician to repair exposed wiring.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 140,
                                            "text": "Hire a licensed electrician to add outlets to rooms that lack them, or that lack a sufficient number of outlets.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 141,
                                            "text": "Use outlet covers to prevent electric shock.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 142,
                                            "text": "Verify or adjust the hot water heater to a maximum of 120F.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 143,
                                            "text": "Have fireplace chimneys and oil flues professionally cleaned annually.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 144,
                                            "text": "Ensure the dryer lint trap is clean and is connected so that it exhausts to the outside.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 145,
                                            "text": "Ensure that fireplaces have screens.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 146,
                                            "text": "Ensure the home has smoke detectors on each floor, preferably hardwired together (local code may require this).",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 147,
                                            "text": "Do not use extension cords as a permanent solution to insufficient electrical outlets.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 148,
                                            "text": "In needed, use power strips with overload protection as a safe alternative.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 149,
                                            "text": "Make sure there are GFCI for all outlets in rooms with water sources.",
                                            "is_selected": False
                                        }
                                        ],
                                        "subcategories": [],
                                        "applicable": True
                                    },
                                    {
                                        "id": 35,
                                        "name": "Occupants(Fires and Burns)",
                                        "order": 35,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [
                                        {
                                            "id": 150,
                                            "text": "Do not smoke inside the home.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 151,
                                            "text": "Have a nonflammable container for ashes and cigarette butts for occupants who smoke outside.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 152,
                                            "text": "Be cautious when using candles.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 153,
                                            "text": "Be cautious when using space heaters.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 154,
                                            "text": "Don’t leave matches or lighters around.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 155,
                                            "text": "Don’t leave wood stoves unattended.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 156,
                                            "text": "Stay in the home when cooking and do not leave cooking food unattended.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 157,
                                            "text": "Keep combustible material (packaging, hand towels) away from heat sources.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 158,
                                            "text": "Test smoke alarms monthly.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 159,
                                            "text": "Develop and practice a fire escape plan.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 160,
                                            "text": "Add anti-scald devices to faucets and shower heads.",
                                            "is_selected": False
                                        }
                                        ],
                                        "subcategories": [],
                                        "applicable": True
                                    },
                                    {
                                        "id": 36,
                                        "name": "Occupants(Chocking and Suffocation)",
                                        "order": 36,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [
                                        {
                                            "id": 161,
                                            "text": "Ensure balusters on staircases and guardrails on play equipment are less than four inches apart.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 162,
                                            "text": "Ensure cribs meet current CPSC standards.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 163,
                                            "text": "Ensure the mattress is snug to the edges of the crib. If more than two fingers can fit between the mattress and the crib, they are not the correct size match.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 164,
                                            "text": "Use only a mattress and a fitted sheet in a crib. No additional bedding, toys, or stuffed animals are needed.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 165,
                                            "text": "Use a sleep sack, which is a wearable blanket, on an infant in place of other bedding.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 166,
                                            "text": "Do not use fabric “bumpers.”",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 167,
                                            "text": "Do not sleep with an infant; the American Academy of Pediatrics recommends against this.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 168,
                                            "text": "Keep the crib away from window treatments. An infant could use them for leverage while standing and pull them into the crib.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 169,
                                            "text": "Do not hang anything from the crib or bedposts; this creates a strangulation hazard.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 170,
                                            "text": "Use cordless blinds or tie loose ends well out of reach of children.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 171,
                                            "text": "Remove old appliances such as refrigerators, washers, and dryers in which children could become trapped and suffocate.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 172,
                                            "text": "Buy nondescript magnets for the refrigerator and place them out of children’s reach.",
                                            "is_selected": False
                                        }
                                        ],
                                        "subcategories": [],
                                        "applicable": True
                                    },
                                    {
                                        "id": 37,
                                        "name": "Environment(Drowning)",
                                        "order": 37,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [
                                        {
                                            "id": 173,
                                            "text": "Follow local codes on pool safety, which typically requires a fence with a locking gate.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 174,
                                            "text": "Add fences around, or safety nets over, water features such as ponds.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 175,
                                            "text": "Use a cover with locking straps when a hot tub is not in use.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 176,
                                            "text": "Protect steps to hot tubs or above-ground pools with locking gates.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 177,
                                            "text": "If steps are movable, move them away from the hot tub or above-ground pool and chain-lock them to a fixed object such as a fence post when they are not in use.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 178,
                                            "text": "Cap old, unused wells according to local building code.",
                                            "is_selected": False
                                        }
                                        ],
                                        "subcategories": [],
                                        "applicable": True
                                    },
                                    {
                                        "id": 38,
                                        "name": "Occupants(Drowning)",
                                        "order": 38,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [
                                        {
                                            "id": 179,
                                            "text": "Properly store buckets, wheelbarrows, and any other item that could collect water.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 180,
                                            "text": "Lock (don’t just latch) pool gates.",
                                            "is_selected": False
                                        }
                                        ],
                                        "subcategories": [],
                                        "applicable": True
                                    },
                                    {
                                        "id": 39,
                                        "name": "Environment(Other Hazards)",
                                        "order": 39,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [
                                        {
                                            "id": 181,
                                            "text": "Avoid using fencing that has sharp points or jagged edges at the top. Certain styles of chain link, picket, stockade, and wrought-iron fencing may fall into this category.",
                                            "is_selected": False
                                        }
                                        ],
                                        "subcategories": [],
                                        "applicable": True
                                    },
                                    {
                                        "id": 40,
                                        "name": "Occupants(Other Hazards)",
                                        "order": 40,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [
                                        {
                                            "id": 182,
                                            "text": "Cover exposed nuts and bolts on play structures and picnic benches to prevent cuts and scrapes.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 183,
                                            "text": "Place stickers or some other marker on glass doors so that occupants will see they are closed.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 184,
                                            "text": "Use outlet covers in homes with young children to prevent electrocution.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 185,
                                            "text": "Use doorknob covers and door locks to prevent children from accessing rooms with dangers.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 186,
                                            "text": "Use door stops and door holders to prevent children’s fingers from being pinched.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 187,
                                            "text": "Use corner and edge bumpers to help prevent injuries.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 188,
                                            "text": "Keep refrigerators at 40F or lower.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 189,
                                            "text": "Store raw and cooked food in separate containers.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 190,
                                            "text": "Wash hands before handling food and again after handling raw meat or seafood.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 191,
                                            "text": "Use a food thermometer to ensure food has been cooked to a safe temperature.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 192,
                                            "text": "Store firearms unloaded, locked, and in a gun safe.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 193,
                                            "text": "Store ammunition in a separate location than the firearms.",
                                            "is_selected": False
                                        }
                                        ],
                                        "subcategories": [],
                                        "applicable": True
                                    }
                                    ]
                                },
                                {
                                    "principle": {
                                    "id": 6,
                                    "created_at": "2023-01-01T00:00:00+00:00",
                                    "updated_at": "2023-01-01T00:00:00+00:00",
                                    "name": "Keep It Ventilated",
                                    "order": 6,
                                    "key": "VENTILATED"
                                    },
                                    "categories": [
                                    {
                                        "id": 41,
                                        "name": "Mechanical",
                                        "order": 41,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [],
                                        "subcategories": [
                                        {
                                            "id": 42,
                                            "name": "Heating Systems",
                                            "order": 42,
                                            "is_answered": False,
                                            "feedback": None,
                                            "options": [
                                            {
                                                "id": 194,
                                                "text": "If possible, do not use a fireplace or wood stove as the primary source of heat.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 195,
                                                "text": "If possible, replace a wood-burning fireplace with a properly vented gas fireplace.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 196,
                                                "text": "Install CO alarms near sleeping areas and on every level of the home.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 197,
                                                "text": "Follow the manufacturer’s recommendation on whether to place it on the wall or a ceiling.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 198,
                                                "text": "Seal leaks in ducts.",
                                                "is_selected": False
                                            }
                                            ],
                                            "subcategories": [],
                                            "applicable": True
                                        },
                                        {
                                            "id": 43,
                                            "name": "Bathrooms",
                                            "order": 43,
                                            "is_answered": False,
                                            "feedback": None,
                                            "options": [
                                            {
                                                "id": 199,
                                                "text": "Locate an exhaust fan in each bathroom.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 200,
                                                "text": "Ensure the fan vents to the outside, not the attic, to prevent moisture problems.",
                                                "is_selected": False
                                            }
                                            ],
                                            "subcategories": [],
                                            "applicable": True
                                        },
                                        {
                                            "id": 44,
                                            "name": "Kitchens",
                                            "order": 44,
                                            "is_answered": False,
                                            "feedback": None,
                                            "options": [
                                            {
                                                "id": 201,
                                                "text": "Locate an exhaust fan (not a recirculating fan) above the range.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 202,
                                                "text": "Ensure a quiet fan is chosen, otherwise occupants may not use it.",
                                                "is_selected": False
                                            }
                                            ],
                                            "subcategories": [],
                                            "applicable": True
                                        },
                                        {
                                            "id": 45,
                                            "name": "Clothes Dryer",
                                            "order": 45,
                                            "is_answered": False,
                                            "feedback": None,
                                            "options": [
                                            {
                                                "id": 203,
                                                "text": "Ensure dryers are connected to a vent that exhausts outside (except for a heat pump dryer).",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 204,
                                                "text": "Ensure dryer vent exhaust is working, is clean and free of lint, and is not leaking.",
                                                "is_selected": False
                                            }
                                            ],
                                            "subcategories": [],
                                            "applicable": True
                                        },
                                        {
                                            "id": 46,
                                            "name": "General",
                                            "order": 46,
                                            "is_answered": False,
                                            "feedback": None,
                                            "options": [
                                            {
                                                "id": 205,
                                                "text": "Use whole-house ventilation to supply fresh air to the home, dilute indoor air, and remove contaminated air.",
                                                "is_selected": False
                                            }
                                            ],
                                            "subcategories": [],
                                            "applicable": True
                                        }
                                        ],
                                        "applicable": True
                                    },
                                    {
                                        "id": 47,
                                        "name": "Occupants",
                                        "order": 47,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [],
                                        "subcategories": [
                                        {
                                            "id": 48,
                                            "name": "Heating Systems",
                                            "order": 48,
                                            "is_answered": False,
                                            "feedback": None,
                                            "options": [
                                            {
                                                "id": 206,
                                                "text": "Have the heating system serviced by a professional annually.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 207,
                                                "text": "For wood and oil-burning systems, have the flue cleaned by a professional annually.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 208,
                                                "text": "Change the furnace/HVAC filter regularly.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 209,
                                                "text": "Do not use unvented kerosene or gas heaters, which can generate CO.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 210,
                                                "text": "Have the fireplace flue cleaned by a professional annually.",
                                                "is_selected": False
                                            }
                                            ],
                                            "subcategories": [],
                                            "applicable": True
                                        },
                                        {
                                            "id": 49,
                                            "name": "Bathrooms",
                                            "order": 49,
                                            "is_answered": False,
                                            "feedback": None,
                                            "options": [
                                            {
                                                "id": 211,
                                                "text": "Turn on the fan when the bathtub or shower is being used.",
                                                "is_selected": False
                                            }
                                            ],
                                            "subcategories": [],
                                            "applicable": True
                                        },
                                        {
                                            "id": 50,
                                            "name": "Kitchens",
                                            "order": 50,
                                            "is_answered": False,
                                            "feedback": None,
                                            "options": [
                                            {
                                                "id": 212,
                                                "text": "Turn on the fan when the range is being used.",
                                                "is_selected": False
                                            },
                                            {
                                                "id": 213,
                                                "text": "Establish a cleaning routine to address the grease that collects on the fan grille.",
                                                "is_selected": False
                                            }
                                            ],
                                            "subcategories": [],
                                            "applicable": True
                                        },
                                        {
                                            "id": 51,
                                            "name": "General",
                                            "order": 51,
                                            "is_answered": False,
                                            "feedback": None,
                                            "options": [
                                            {
                                                "id": 214,
                                                "text": "Never idle a car in an attached garage, even with the garage door open.",
                                                "is_selected": False
                                            }
                                            ],
                                            "subcategories": [],
                                            "applicable": True
                                        }
                                        ],
                                        "applicable": True
                                    },
                                    {
                                        "id": 52,
                                        "name": "Building",
                                        "order": 52,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [
                                        {
                                            "id": 215,
                                            "text": "Air seal the home to help control where air infiltrates and ex-filtrates.",
                                            "is_selected": False
                                        }
                                        ],
                                        "subcategories": [],
                                        "applicable": True
                                    }
                                    ]
                                },
                                {
                                    "principle": {
                                    "id": 7,
                                    "created_at": "2023-01-01T00:00:00+00:00",
                                    "updated_at": "2023-01-01T00:00:00+00:00",
                                    "name": "Keep It Comfortable",
                                    "order": 7,
                                    "key": "COMFORTABLE"
                                    },
                                    "categories": [
                                    {
                                        "id": 53,
                                        "name": "Environment",
                                        "order": 53,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [
                                        {
                                            "id": 216,
                                            "text": "Maintain the home at WHO-recommended temperatures for the occupants.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 217,
                                            "text": "Set the temperature on the programmable thermostat to be lower (in heating seasons) or higher (in cooling seasons) when occupants aren’t home.",
                                            "is_selected": False
                                        }
                                        ],
                                        "subcategories": [],
                                        "applicable": True
                                    },
                                    {
                                        "id": 54,
                                        "name": "Building",
                                        "order": 54,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [
                                        {
                                            "id": 218,
                                            "text": "Air seal in the basement and attic (if these are unconditioned spaces) to establish a pressure boundary. This controls airflow and reduces convective heat transfer.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 219,
                                            "text": "Install weatherstrip around windows and window frames, and doors and door frames, to establish a pressure boundary.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 220,
                                            "text": "Install door sweeps along the bottom of entry doors to establish a pressure boundary.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 221,
                                            "text": "Install insulation in unconditioned spaces to establish a thermal boundary. This reduces conductive heat transfer.",
                                            "is_selected": False
                                        }
                                        ],
                                        "subcategories": [],
                                        "applicable": True
                                    },
                                    {
                                        "id": 55,
                                        "name": "Mechanicals",
                                        "order": 55,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [
                                        {
                                            "id": 222,
                                            "text": "Air seal duct systems to control airflow and reduce convective heat transfer.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 223,
                                            "text": "Ensure the heating and cooling systems are adequate for the home.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 224,
                                            "text": "Install a programmable thermostat.",
                                            "is_selected": False
                                        }
                                        ],
                                        "subcategories": [],
                                        "applicable": True
                                    },
                                    {
                                        "id": 56,
                                        "name": "Occupants",
                                        "order": 56,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [
                                        {
                                            "id": 225,
                                            "text": "Investigate assistance programs for low-income households, such as Low Income Home Energy Assistance Program (LIHEAP)(https://www.acf.hhs.gov/ocs/resource/division-of-energy-assistance-federal-staff).",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 226,
                                            "text": "Have the heating/cooling systems maintained annually.",
                                            "is_selected": False
                                        }
                                        ],
                                        "subcategories": [],
                                        "applicable": True
                                    }
                                    ]
                                },
                                {
                                    "principle": {
                                    "id": 8,
                                    "created_at": "2023-01-01T00:00:00+00:00",
                                    "updated_at": "2023-01-01T00:00:00+00:00",
                                    "name": "Keep It Maintained",
                                    "order": 8,
                                    "key": "MANTAINED"
                                    },
                                    "categories": [
                                    {
                                        "id": 57,
                                        "name": "The Hazards of LEAD, ASBESTOS, and RADON in the home",
                                        "order": 57,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [
                                        {
                                            "id": 227,
                                            "text": "Other toxic elements include: Mercury and Sewer gas",
                                            "is_selected": False
                                        }
                                        ],
                                        "subcategories": [],
                                        "applicable": True
                                    },
                                    {
                                        "id": 58,
                                        "name": "Six Steps to Maintaining a Healthy Home",
                                        "order": 58,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [
                                        {
                                            "id": 228,
                                            "text": "Identify what needs to be done.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 229,
                                            "text": "Determine level of ability required for tasks and projects. For example, are homeowners comfortable climbing a ladder? Is help needed to move furniture in order to clean or make a repair? When is a licensed professional needed?",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 230,
                                            "text": "Schedule time for maintenance of areas or appliances identified. Be realistic in blocking out time on a calendar, just like one might for any other activity important to good family health. For many people, committing to a regular maintenance schedule is often an overlooked step.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 231,
                                            "text": "Prioritize work by season. Developing a checklist for each season in your part of the country can be a useful tool.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 232,
                                            "text": "Plan for each activity and assemble the tools, and if needed, the people, to complete the scheduled maintenance activity.",
                                            "is_selected": False
                                        },
                                        {
                                            "id": 233,
                                            "text": "Check tasks off the list as they are completed. Satisfaction guaranteed!!",
                                            "is_selected": False
                                        }
                                        ],
                                        "subcategories": [],
                                        "applicable": True
                                    }
                                    ]
                                },
                                {
                                    "principle": {
                                    "id": 9,
                                    "created_at": "2023-01-01T00:00:00+00:00",
                                    "updated_at": "2023-01-01T00:00:00+00:00",
                                    "name": "Final Recommendations",
                                    "order": 9,
                                    "key": "FINAL"
                                    },
                                    "categories": [
                                    {
                                        "id": 59,
                                        "name": "Final Remarks",
                                        "order": 59,
                                        "is_answered": False,
                                        "feedback": None,
                                        "options": [],
                                        "subcategories": [],
                                        "applicable": True
                                    }
                                    ]
                                }
                                ]
                            }
        return context

# Home Energy Side templates

class ExteriorEvaluationFuelLeakTestingPageTemplateView(LoginRequiredMixin, TemplateView):
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