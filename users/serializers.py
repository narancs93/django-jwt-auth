from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["email"] = user.email

        return token


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "confirm_password"]
        extra_kwargs = {"password": {"write_only": True}, "email": {"required": True}}

    def validate(self, data):
        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data, is_active=False)
        return user
