from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    class Meta:
        model = User
        fields = ["email", "tg_chat_id", "password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }


