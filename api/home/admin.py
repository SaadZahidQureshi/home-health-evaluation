from django.contrib import admin
from .models import *

admin.site.register(Principle)
admin.site.register(Option)
admin.site.register(SelectedOption)
admin.site.register(Feedback)
admin.site.register(Category)
admin.site.register(CategoryApplicability)

