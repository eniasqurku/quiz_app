from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.fields import CharField
from rest_framework.serializers import Serializer
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from six import text_type

from agent.cons import CREATOR_GROUP_ID, PARTICIPANT_GROUP_ID
from agent.models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def update(self, instance, validated_data):
        return super(MyTokenObtainPairSerializer, self).update(instance, validated_data)

    def create(self, validated_data):
        return super(MyTokenObtainPairSerializer, self).create(validated_data)

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        groups = list(self.user.groups.all().values_list('name', flat=True))
        refresh = self.get_token(self.user)
        data['refresh'] = text_type(refresh)
        data['access'] = text_type(refresh.access_token)
        data['email'] = self.user.email
        data['groups'] = groups
        return data


class ChangePasswordSerializer(Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = CharField(required=True)
    new_password = CharField(required=True)


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        view_kwargs = self.context['view'].kwargs
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        if view_kwargs['creator']:
            user.groups.set([CREATOR_GROUP_ID])
        else:
            user.groups.set([PARTICIPANT_GROUP_ID])

        user.save()

        return user
