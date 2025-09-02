from django.contrib import admin
from .models import Step, Question, Feedback, SelectedOptions, Option, QuestionGroup, Answer

admin.site.register(Step)
admin.site.register(QuestionGroup)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Feedback)
admin.site.register(SelectedOptions)
admin.site.register(Option)