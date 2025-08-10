from django.db import models


class Roles(models.TextChoices):
    ADMIN = "admin", "Admin"
    USER = "user", "User"

class CharFieldSizes(models.IntegerChoices):
    SMALL = 50
    MEDIUM = 100
    LARGE = 255

HOME_TYPES = [
    ('SF', 'Single Family'),
    ('AP', 'Apartment'),
    ('CO', 'Condo'),
    ('TH', 'Townhouse'),
]

DUCT_CONDITION_CHOICES = [
    ('CL', 'Clean'),
    ('DU', 'Dusty'),
    ('MO', 'Moldy'),
    ('PI', 'Pest Infested'),
]

HEATING_SYSTEM_CHOICES = [
    ('FA', 'Forced Air'),
    ('RA', 'Radiator'),
    ('HP', 'Heat Pump'),
    ('OT', 'Other'),
]

ELECTRICAL_CONDITION_CHOICES = [
    ('GO', 'Good'),
    ('FA', 'Fair'),
    ('PO', 'Poor'),
]

SMOKING_POLICY_CHOICES = [
    ('NS', 'No Smoking'),
    ('SO', 'Smoking Outside'),
    ('SI', 'Smoking Inside'),
]

CLUTTER_LEVEL_CHOICES = [
    ('NO', 'None'),
    ('LO', 'Low'),
    ('MO', 'Moderate'),
    ('HI', 'High'),
]

CLEANING_SCHEDULE_CHOICES = [
    ('RE', 'Regular'),
    ('IR', 'Irregular'),
    ('NO', 'None'),
]

SHOE_REMOVAL_CHOICES = [
    ('AL', 'Always'),
    ('SO', 'Sometimes'),
    ('NE', 'Never'),
]

VACUUM_TYPE_CHOICES = [
    ('HE', 'HEPA'),
    ('NH', 'Non-HEPA'),
    ('NO', 'None'),
]

DUSTING_METHOD_CHOICES = [
    ('WE', 'Wet'),
    ('DR', 'Dry'),
    ('NO', 'None'),
]

FLOOR_CLEANING_CHOICES = [
    ('WM', 'Wet Mop'),
    ('DM', 'Dry Mop'),
    ('OT', 'Other'),
]

MAINTENANCE_SCHEDULE_CHOICES = [
    ('RE', 'Regular'),
    ('IR', 'Irregular'),
    ('NO', 'None'),
]

CATEGORY_CHOICES = [
    ('BU', 'Building'),
    ('ME', 'Mechanicals'),
    ('EN', 'Environment'),
    ('OC', 'Occupant'),
    ('PE', 'Pest'),
    ('SA', 'Safety'),
    ('MA', 'Maintenance'),
]

PRIORITY_CHOICES = [
    ('HI', 'High'),
    ('ME', 'Medium'),
    ('LO', 'Low'),
]

CATEGORY_CHOICES = [
    ('BU', 'Building'),
    ('ME', 'Mechanicals'),
    ('EN', 'Environment'),
    ('OC', 'Occupant'),
    ('PE', 'Pest'),
    ('SA', 'Safety'),
    ('MA', 'Maintenance'),
]

CATEGORY_CHOICES = [
    ('CL', 'Clean'),
    ('DR', 'Dry'),
    ('PF', 'Pest-Free'),
    ('CF', 'Contaminant-Free'),
    ('SA', 'Safe'),
    ('VE', 'Ventilated'),
    ('CO', 'Comfortable'),
    ('MA', 'Maintained'),
]
