from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.fields import CharField
from rest_framework.serializers import Serializer
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from agent.cons import CREATOR_GROUP_ID, PARTICIPANT_GROUP_ID
from agent.models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        groups = list(self.user.groups.all().values_list("name", flat=True))
        data["email"] = self.user.email
        data["groups"] = groups

        return data


class ChangePasswordSerializer(Serializer):
    """
    Serializer for password change endpoint.
    """

    old_password = CharField(required=True)
    new_password = CharField(required=True)


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password_repeat = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("password", "password_repeat", "email", "first_name", "last_name")

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs["password"] != attrs["password_repeat"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        view_kwargs = self.context["view"].kwargs
        user = User.objects.create(
            email=validated_data["email"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )

        user.set_password(validated_data["password"])
        if view_kwargs["creator"]:
            user.groups.set([CREATOR_GROUP_ID])
        else:
            user.groups.set([PARTICIPANT_GROUP_ID])

        user.save()

        return user
