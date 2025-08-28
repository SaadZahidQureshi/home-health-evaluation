from django.db import models
from django.contrib.auth import get_user_model
from api.core.abstract import BaseModel
from api.core.choices import *
from api.user.models import Customer
from api.user.models import Photo
User = get_user_model()


class Step(BaseModel):
    title = models.CharField(max_length=CharFieldSizes.LARGE)
    order = models.PositiveIntegerField()


class Question(BaseModel):
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()  
    field_type = models.CharField(
        max_length=CharFieldSizes.SMALL,
        choices=QuestionFieldType.choices,
        default=QuestionFieldType.TEXT,
    )
    options = models.JSONField(blank=True, null=True)


class Response(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="responses")
    images = models.ManyToManyField(Photo, related_name="response_images")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer_response")
    text_answer = models.TextField(blank=True, null=True)
    numeric_answer = models.FloatField(blank=True, null=True)
    selected_option = models.CharField(max_length=CharFieldSizes.LARGE, blank=True, null=True)
