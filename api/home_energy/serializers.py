from rest_framework import serializers
from .models import *


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ["id", "order", "title"]


class ShortQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["id", "text"]


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["id", "text", "field_type", "options"]


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["id", "image"]


class FeedbackSerializer(serializers.ModelSerializer):
    images = PhotoSerializer(many=True, read_only=True)
    image_ids = serializers.PrimaryKeyRelatedField(queryset=Photo.objects.all(), many=True, write_only=True, required=False)

    class Meta:
        model = Feedback
        fields = ["id", "question", "customer", "text_answer", "numeric_answer", "selected_option", "images", "image_ids"]

    def create(self, validated_data):
        image_ids = validated_data.pop("image_ids", [])
        response = Feedback.objects.create(**validated_data)
        response.images.set(image_ids)
        return response


class FeedbackSerializer(serializers.ModelSerializer):
    images = PhotoSerializer(many=True, read_only=True)
    class Meta:
        model = Feedback
        fields = ["id", "question_group", "customer", "text","images"]



# -----------------------------------

class OptionWithSelectionSerializer(serializers.ModelSerializer):
    is_selected = serializers.BooleanField()

    class Meta:
        model = Option
        fields = ["id", "text", "is_selected"]


class QuestionWithOptionsSerializer(serializers.ModelSerializer):
    options = OptionWithSelectionSerializer(many=True)
    is_answered = serializers.BooleanField(default=False)

    class Meta:
        model = Question
        fields = ["id", "text", "field_type", "is_answered", "options"]


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ["id", "text"]


class QuestionAnswerSerializer(serializers.Serializer):
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    text = serializers.CharField(required=False, default='', allow_blank=True)


class HomeEnergyAnswerSerializer(serializers.Serializer):
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    text = serializers.CharField(required=False, default='', allow_blank=True)


class SelectionSerializer(serializers.Serializer):
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    selected_options = serializers.ListField(child=serializers.IntegerField(), required=True, allow_empty=False)


class ShortQuestionGroupSerialzier(serializers.ModelSerializer):
    class Meta:
        model = QuestionGroup
        fields = "__all__"


class QuestionGroupSerialzier(serializers.ModelSerializer):
    question = QuestionSerializer(many=True)
    feedback = serializers.SerializerMethodField()
    class Meta:
        model = QuestionGroup
        fields = ["id", "step", "question", "feedback"]

    
    def get_feedback(self, obj):
        customer = Customer.objects.get(id=self.context.get("customer_id"))
        feedbacks = Feedback.objects.filter(customer=customer, question_group=obj)
        return FeedbackSerializer(feedbacks, many=True).data

class UploadImagesResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    feedback = serializers.JSONField()

    