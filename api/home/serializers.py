from rest_framework import serializers
from .models import *


class PrincipleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Principle
        fields = "__all__"


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class PestTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PestType
        fields = "__all__"


class QuestionGroupSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer()
    pest_type = PestTypeSerializer()

    class Meta:
        model = QuestionGroup
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    principle = PrincipleSerializer()
    group = QuestionGroupSerializer()
    category = CategoriesSerializer()
    pest_type = PestTypeSerializer()

    class Meta:
        model = Question
        fields = "__all__"


class ShortQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = "__all__"


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'image', 'customer']


class AnswerSerializer(serializers.ModelSerializer):
    images = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'question', 'details', 'images', 'created_at', 'updated_at']


class ShortAnswerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Answer
        fields = ['id', 'question', 'details']


class ReturnShortAnswerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Answer
        fields = ['id', 'question', 'details', "customer"]


class ReturnCustomerSerializer(serializers.ModelSerializer):
    user = ShortUserSerializer()
    class Meta:
        model = Customer
        fields = "__all__"

class CustomerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name')  
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Customer
        fields = ["name", "email", "address", "city", "state", "zip", "house_image", "audit_completed"]

    def update(self, instance, validated_data):
        user_serializer = ShortUserSerializer(instance=instance.user, data=validated_data.pop('user'), partial=True)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        validated_data['user'] = user
        validated_data["audit_completed"] = True
        return super().update(instance, validated_data)
