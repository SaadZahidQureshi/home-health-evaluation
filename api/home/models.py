from django.db import models
from django.contrib.auth import get_user_model
from api.core.abstract import BaseModel
from api.core.choices import *
from api.user.serializers import ShortUserSerializer
User = get_user_model()


class Customer(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_user")
    house_image = models.ImageField(upload_to="house_images/", null=True, blank=True)
    address = models.CharField(max_length=CharFieldSizes.LARGE, null=True)
    city = models.CharField(max_length=CharFieldSizes.SMALL, null=True)
    state = models.CharField(max_length=CharFieldSizes.SMALL, null=True)
    zip = models.CharField(max_length=CharFieldSizes.SMALL, null=True)
    audit_completed = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_created_by")

    @classmethod
    def create_default_customer(self, obj):
        user_data = {
            "name": None,
            "email": None,
            "role": Roles.CUSTOMER
        }
        user_serializer = ShortUserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        return self.objects.create(user=user,address=None,city=None,state=None,zip=None, created_by=obj)


class Principle(BaseModel):
    name = models.CharField(max_length=CharFieldSizes.LARGE)
    order = models.PositiveIntegerField(default=0)
    key = models.CharField(max_length=CharFieldSizes.LARGE)

    class Meta:
        ordering = ['order']


class Category(BaseModel):
    principle = models.ForeignKey(Principle, on_delete=models.CASCADE, null=True, related_name="categories")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=CharFieldSizes.LARGE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Categories"

    def is_subcategory(self):
        return self.parent is not None
    
    def get_main_category(self):
        if self.parent:
            return self.parent.get_main_category()
        return self

class CategoryApplicability(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="category_applicabilities")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="applicabilities")
    applicable = models.BooleanField(default=True)

    class Meta:
        unique_together = ("customer", "category")


class Option(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=CharFieldSizes.LARGE)


class SelectedOption(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="selected_options")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="selected_options")
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    selected = models.BooleanField(default=False)

    class Meta:
        unique_together = ("customer", "option")


class Photo(BaseModel):
    image = models.ImageField(upload_to='answer_photos/')

    def __str__(self):
        return f"Photo {self.id}"

class Feedback(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="feedbacks")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="feedback")
    images = models.ManyToManyField(Photo, related_name="answer_images")
    note = models.TextField(blank=True)
