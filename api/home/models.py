from django.db import models
from django.contrib.auth import get_user_model
from api.core.abstract import BaseModel
from api.core.choices import *
from api.user.serializers import ShortUserSerializer
User = get_user_model()

class Principle(BaseModel):
    PRINCIPLE_CHOICES = [
        ('CLEAN', 'Clean'),
        ('DRY', 'Dry'),
        ('PESTFREE', 'Pest-Free'),
        ('CONTAMINANTFREE', 'Contaminant-Free'),
        ('SAFE', 'Safe'),
        ('VENTILATED', 'Ventilated'),
        ('COMFORTABLE', 'Comfortable'),
        ('MANTAINED', 'Maintained'),
    ]
    key = models.CharField(max_length=CharFieldSizes.SMALL, choices=PRINCIPLE_CHOICES, unique=True)
    name = models.CharField(max_length=CharFieldSizes.SMALL)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class PestType(BaseModel):
    PEST_CHOICES = [
        ('RODENTS', 'Rodents'),
        ('COCKROACHES', 'Cockroaches'),
        ('DUST_MITES', 'Dust Mites'),
        ('BED_BUGS', 'Bed Bugs'),
    ]
    key = models.CharField(max_length=CharFieldSizes.SMALL, choices=PEST_CHOICES, unique=True)
    name = models.CharField(max_length=CharFieldSizes.SMALL)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Category(BaseModel):
    CATEGORY_CHOICES = [
        ('BUILDING', 'Building'),
        ('MECHANICALS', 'Mechanicals'),
        ('ENVIRONMENT', 'Environment'),
        ('OCCUPANT', 'Occupant'),
    ]
    key = models.CharField(max_length=CharFieldSizes.SMALL, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=CharFieldSizes.SMALL)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class QuestionGroup(BaseModel):
    name = models.CharField(max_length=CharFieldSizes.SMALL)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    pest_type = models.ForeignKey(PestType, on_delete=models.CASCADE, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ('category', 'pest_type', 'name')

    def __str__(self):
        if self.pest_type:
            return f"{self.category.name} - {self.pest_type.name}: {self.name}"
        return f"{self.category.name}: {self.name}"


class Question(BaseModel):
    principle = models.ForeignKey(Principle, on_delete=models.CASCADE)
    group = models.ForeignKey(QuestionGroup, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    pest_type = models.ForeignKey(PestType, on_delete=models.CASCADE, null=True, blank=True) 
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if self.group:
            self.category = self.group.category
            self.pest_type = self.group.pest_type
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.principle.name} - {self.category.name}: {self.text[:50]}..."


class Customer(BaseModel):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    house_image = models.ImageField(upload_to="house_images/", null=True, blank=True)
    address = models.CharField(CharFieldSizes.LARGE, null=True)
    city = models.CharField(CharFieldSizes.SMALL, null=True)
    state = models.CharField(CharFieldSizes.SMALL, null=True)
    zip = models.CharField(CharFieldSizes.SMALL, null=True)

    @classmethod
    def create_default_customer(cls):
        user_data = {
            "name": None,
            "email": None,
            "role": Roles.CUSTOMER
        }
        user_serializer = ShortUserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        return cls.objects.create(user=user,address=None,city=None,state=None,zip=None)


class Answer(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    details = models.TextField(blank=True)
    images = models.ManyToManyField('Photo')

    def __str__(self):
        return f"Answer for {self.question}"


class Photo(BaseModel):
    image = models.ImageField(upload_to='answer_photos/')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Photo {self.id}"
