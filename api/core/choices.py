from django.db import models


class Roles(models.TextChoices):
    ADMIN = "admin", "Admin"
    USER = "user", "User"
    CUSTOMER = "customer", "Customer"

class CustomerTypes(models.TextChoices):
    HEALTHY_HOME = "healthy_home", "Healthy Home"
    RESIDENTIAL_HOME = "residential_home", "Residential Home"

class CharFieldSizes(models.IntegerChoices):
    SMALL = 50
    MEDIUM = 100
    LARGE = 255

QUESTION_CHOICES=[
    ("text", "Text"),
    ("number", "Number"),
    ("dropdown", "Dropdown"),
    ("comment", "Comment"),
    ("image", "Image"),
],

class QuestionFieldType(models.TextChoices):
    TEXT = "text", "Text",
    NUMBER = "number", "Number",
    DROPDOWN = "dropdown", "Dropdown"