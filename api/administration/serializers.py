from django.contrib.auth import authenticate, get_user_model

from rest_framework import serializers

from api.core.choices import Roles
from api.core.validators import DotsValidationError
from .models import TokenManagement


User = get_user_model()


class LoginAdminSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(request=self.context.get('request'), username=email, password=password)
        if not user:
            raise DotsValidationError("User not found.")
        if user.role != Roles.ADMIN:
            raise DotsValidationError("You are not authorized to log in here")
        attrs['user'] = user
        return attrs
    


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenManagement
        fields = ["id", "email", "token", "is_used", "created_at", "updated_at"]
        read_only_fields = ["token", "is_used", "created_at", "updated_at"]

    def create(self, validated_data):
        email = validated_data["email"].lower()

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "User already registered with this email."})
        
        existing = TokenManagement.objects.filter(email=email, is_used=False).first()
        if existing:
            raise serializers.ValidationError(
                {"error": "Token already exists and is not used yet. Use regenerate instead."}
            )

        # generate new token
        token = TokenManagement.generate_token()
        validated_data["token"] = token
        return super().create(validated_data)


class TokenRegenerateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenManagement
        fields = ["email", "token", "is_used", "created_at"]
        read_only_fields = ["token", "is_used", "created_at"]

    def create(self, validated_data):
        email = validated_data["email"]

        # delete existing unused token
        TokenManagement.objects.filter(email=email, is_used=False).delete()

        # generate new token
        validated_data["token"] = TokenManagement.generate_token()
        return TokenManagement.objects.create(**validated_data)
