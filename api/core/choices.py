from django.db import models


class Roles(models.TextChoices):
    ADMIN = "admin", "Admin"
    USER = "user", "User"
    CUSTOMER = "customer", "Customer"

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
    DROPDOWN = "dropdown", "Dropdown",
    COMMENT = "comment", "Comment",
    IMAGE = "image", "Image",