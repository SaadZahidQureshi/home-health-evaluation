from django.contrib import admin

# Register your models here.

from .models import Availability, BookingPerson, Appointment

admin.site.register(BookingPerson)
admin.site.register(Appointment)
