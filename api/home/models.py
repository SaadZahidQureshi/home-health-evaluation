from django.db import models
from django.contrib.auth import get_user_model
from api.core.abstract import BaseModel
from api.core.choices import *
from api.user.models import Photo, Customer
User = get_user_model()

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


class CategoryApplicability(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="category_applicabilities")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="applicabilities")
    applicable = models.BooleanField(default=True)

    class Meta:
        unique_together = ("customer", "category")


class Option(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=CharFieldSizes.LARGE)


class SelectedOption(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer_selected_options")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_selected_options")
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    selected = models.BooleanField(default=False)

    class Meta:
        unique_together = ("customer", "option")


class Feedback(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="feedbacks")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="feedback")
    images = models.ManyToManyField(Photo, related_name="feedback_images")
    note = models.TextField(blank=True)