from rest_framework.serializers import ModelSerializer

from agent.models import User


class UserReadSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "is_active",
        ]
