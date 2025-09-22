from hmac import compare_digest
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate, login
from api.core.choices import Roles
from api.core.validators import PasswordValidator, DotsValidationError, phone_regex
from .models import Photo, Customer
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "phone", "role", "is_active", "image"]


class RegisterUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[
            PasswordValidator.one_symbol,
            PasswordValidator.lower_letter,
            PasswordValidator.upper_letter,
            PasswordValidator.number,
            PasswordValidator.length,
        ],
    )
    class Meta:
        model = User
        fields = ["name", "email", "password", "confirm_password"]

    def get_fields(self):
        fields = super().get_fields()
        if self.instance:
            fields['phone'] = serializers.CharField(
                max_length=20,
                validators=[phone_regex],
                required=False,
                allow_null=True,
                allow_blank=True
            )
            fields['image'] = serializers.ImageField(
                required=False,
                allow_null=True,
            )
        return fields
    
    def validate(self, attrs):
        if not self.instance:
            password = attrs.get("password")
            confirm_password = attrs.pop("confirm_password")
            if not compare_digest(password, confirm_password):
                raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        validated_data.pop('password', None)
        validated_data.pop('confirm_password', None)
        image = validated_data.pop('image', None)
        phone = validated_data.get('phone', None)
        if phone:
            if User.objects.exclude(id=instance.id).filter(phone=phone).exists():
                raise serializers.ValidationError({"phone": "This phone number is already in use."})
        if image is not None:
            instance.image = image
        return super().update(instance, validated_data)
    

class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(request=self.context.get('request'), username=email, password=password)
        if not user:
            raise DotsValidationError("User not found.")
        if user.role != Roles.USER:
            raise DotsValidationError("You are not authorized to log in here")
        attrs['user'] = user
        return attrs
    

class ShortUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["name", "email", "role"]


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[
            PasswordValidator.one_symbol,
            PasswordValidator.lower_letter,
            PasswordValidator.upper_letter,
            PasswordValidator.number,
            PasswordValidator.length,
        ],
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        user = self.context['request'].user
        if not compare_digest(attrs['new_password'], attrs['confirm_password']):
            raise serializers.ValidationError({"new_password": "New password and confirm password do not match"})
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({"old_password": "Old password is incorrect"})
        if attrs['new_password'] == attrs['old_password']:
            raise serializers.ValidationError({"new_password": "New password cannot be the same as old password"}) 
        return attrs
    
    def update(self, instance, validated_data):
        new_password = validated_data.get('new_password')
        instance.set_password(new_password)
        instance.save()
        request = self.context.get('request')
        if request:
            login(request, instance)
        return instance


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
    

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = "__all__"