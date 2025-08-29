from django.db import models
from django.contrib.auth import get_user_model
from api.core.abstract import BaseModel
from api.core.choices import *
from api.user.models import Customer, Photo
User = get_user_model()


class Step(BaseModel):
    title = models.CharField(max_length=CharFieldSizes.LARGE)
    order = models.PositiveIntegerField()


class Question(BaseModel):
    text = models.TextField(blank=True, null=True)
    field_type = models.CharField(max_length=CharFieldSizes.SMALL, choices=QuestionFieldType.choices, default=QuestionFieldType.TEXT)


class Answer(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer_answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="question_answers")
    text = models.TextField(blank=True, null=True)


class QuestionGroup(BaseModel):
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name="question_group")
    question = models.ManyToManyField(Question, related_name="question_group_questions")


class Option(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.TextField(blank=True, null=True)


class SelectedOptions(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="home_energy_customer_selected_options")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="home_energy_customer_selected_options_question", null=True, blank=True)
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="home_energy_selected_options")


class Feedback(BaseModel):
    question_group = models.ForeignKey(QuestionGroup, on_delete=models.CASCADE, related_name="responses", null=True, blank=True)
    images = models.ManyToManyField(Photo, related_name="response_images")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer_response")
    text = models.TextField(blank=True, null=True)
