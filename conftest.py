import pytest
from django.contrib.auth.models import Group
from model_bakery import baker
from rest_framework.test import APIClient

from agent.cons import CREATOR_GROUP_NAME, PARTICIPANT_GROUP_NAME
from agent.models import User
from authentication.serializers import MyTokenObtainPairSerializer


@pytest.fixture(autouse=True)
def create_groups(db):
    Group.objects.create(name=CREATOR_GROUP_NAME)
    Group.objects.create(name=PARTICIPANT_GROUP_NAME)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user(faker, api_client):
    user = User(email=faker.email(), is_superuser=True)
    user.set_password(faker.password())
    user.save()

    token = generate_user_token(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    return user


@pytest.fixture
def participant_user(faker, api_client):
    user = User(email=faker.email())
    user.set_password(faker.password())
    user.save()
    group, created = Group.objects.get_or_create(name=PARTICIPANT_GROUP_NAME)
    group.user_set.add(user)
    user.save()

    token = generate_user_token(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    return user


@pytest.fixture
def creator_user(faker, api_client):
    user = User(email=faker.email())
    user.set_password(faker.password())
    user.save()
    group, created = Group.objects.get_or_create(name=CREATOR_GROUP_NAME)
    group.user_set.add(user)
    user.save()

    token = generate_user_token(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    return user


def generate_user_token(user):
    return MyTokenObtainPairSerializer.get_token(user).access_token


@pytest.fixture
def create_quizzes():
    return baker.make('quiz.Quiz', _quantity=5)
