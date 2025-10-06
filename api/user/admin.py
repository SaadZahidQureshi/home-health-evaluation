from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "phone", "is_active", "role"]
    search_fields = ["email", "phone", "role", "name"]
    list_filter = ["is_active"]

admin.site.register(Photo)
admin.site.register(Customer)