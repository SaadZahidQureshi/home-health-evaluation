from django.db import models
from django.core.validators import EmailValidator
from api.core.abstract import BaseModel

class Availability(BaseModel):     
    SLOT_CHOICES = [
        ('08_00_to_12_00', '08:00 AM to 12:00 PM'),
        ('01_00_to_05_00', '01:00 PM to 05:00 PM'),
        # ('05_00_to_09_00', '05:00 PM to 09:00 PM'),
        # ('10_00_to_02_00', '10:00 PM to 02:00 AM'),
        # ('02_00_to_06_00', '02:00 AM to 06:00 AM'),
        # ('07_00_to_11_00', '07:00 AM to 11:00 AM'),
        # ('11_00_to_03_00', '11:00 AM to 03:00 PM'),
        # ('04_00_to_08_00', '04:00 PM to 08:00 PM'),
    ]          
    slot_type = models.CharField(max_length=20, choices=SLOT_CHOICES)     
    date = models.DateField()     
    is_booked = models.BooleanField(default=False)          
    
    class Meta:         
        unique_together = ['slot_type', 'date']          
    
    def __str__(self):         
        return f"{self.get_slot_type_display()} - {self.date}"

class BookingPerson(BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator()])
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Appointment(BaseModel):
    booking_person = models.ForeignKey(BookingPerson, on_delete=models.CASCADE)
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Appointment for {self.booking_person} on {self.availability.date}"
