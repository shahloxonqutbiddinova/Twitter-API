from rest_framework import serializers
from api.models import User


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
