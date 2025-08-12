from hmac import compare_digest
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from api.core.choices import Roles
from api.core.validators import PasswordValidator, DotsValidationError, phone_regex
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