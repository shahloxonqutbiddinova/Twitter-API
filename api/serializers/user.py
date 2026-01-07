from rest_framework import serializers
from api.models import User, DONE
from api.utils import is_email


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        user = User.objects.filter(email=value).first()

        if user and user.status in ["verified", 'done']:
            raise serializers.ValidationError("Bu email allaqachon tasdiqlangan")

        return value

class CodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=20, required=True)

    def validate_code(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("Kod 6ta raqamdan iborat bo'lishi kk")
        return value

class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    phone = serializers.CharField(max_length=13, required=True)
    first_name = serializers.CharField(max_length=100, required=True)
    last_name = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=20, required=True)
    confirm_password = serializers.CharField(max_length=20, required=True)

    def validate_username(self, value):
        if User.objects.filter(username = value).exists():
            raise serializers.ValidationError("Username already in used")

        return value

    def validate_phone(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Phone number already in used")

        return value

    def validate(self, validated_data):
        password = validated_data.get("password")
        confirm_password = validated_data.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError("Password's didn't match.")
        return validated_data


class LoginSerializer(serializers.Serializer):
    user_input = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True)

    def validate(self, validated_data):
        user_input = validated_data.get("user_input")

        if is_email(user_input):
            user = User.objects.filter(email=user_input).filter(status=DONE).first()
            if user is not None:
                validated_data['username'] = user.username
            else:
                raise serializers.ValidationError("User not found")
        else:
            validated_data['username'] = user_input

        return validated_data
