from rest_framework import serializers
from api.user.serializers import PhotoSerializer
from .models import *


class PrincipleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Principle
        fields = "__all__"


class OptionSerializer(serializers.ModelSerializer):
    is_selected = serializers.BooleanField(read_only=True, default=False)
    
    class Meta:
        model = Option
        fields = ["id", "text", "is_selected"]


class SelectedOptionSerializer(serializers.ModelSerializer):
    option = OptionSerializer(read_only=True)
    
    class Meta:
        model = SelectedOption
        fields = "__all__"


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"


class FeedbackSerializer(serializers.ModelSerializer):
    images = PhotoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Feedback
        fields = ["id", "note", "images"]


class CategorySerializer(serializers.ModelSerializer):
    is_answered = serializers.SerializerMethodField()
    feedback = serializers.SerializerMethodField()
    options = OptionSerializer(many=True, read_only=True)
    subcategories = serializers.SerializerMethodField()
    applicable = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Category
        fields = ["id", "name", "order", "is_answered", "feedback", "options", "subcategories", "applicable"]
    
    def get_is_answered(self, obj):
        customer = self.context.get('customer')
        if not customer:
            return False
        return SelectedOption.objects.filter(customer=customer, category=obj, selected=True).exists()
    
    def get_feedback(self, obj):
        customer = self.context.get('customer')
        if not customer:
            return None
            
        try:
            feedback = Feedback.objects.prefetch_related('images').get(customer=customer, category=obj)
            return FeedbackSerializer(feedback).data
        except Feedback.DoesNotExist:
            return None
    
    def get_subcategories(self, obj):
        subcategories = obj.subcategories.all().order_by('order')
        return CategorySerializer(subcategories, many=True, context=self.context).data


class PrincipleCategoriesSerializer(serializers.Serializer):
    principle = PrincipleSerializer()
    categories = CategorySerializer(many=True)


class PrincipleStatusSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    status = serializers.CharField()
    completed_categories = serializers.IntegerField()
    total_categories = serializers.IntegerField()
    progress = serializers.CharField()


class AnswerSerializer(serializers.Serializer):
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    note = serializers.CharField(required=False, default='', allow_blank=True)


class SelectionSerializer(serializers.Serializer):
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    selected_options = serializers.ListField(child=serializers.IntegerField(), required=True, allow_empty=False)


class ApplicableSerializer(serializers.Serializer):
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())


class UploadImagesSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    images = serializers.ListField(child=serializers.ImageField(), required=True)


class UploadImagesResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    images = PhotoSerializer(many=True)
    feedback = serializers.JSONField()

