import pytest
from django.urls import reverse
from rest_framework import status

from agent.cons import PARTICIPANT_GROUP_ID, CREATOR_GROUP_ID
from agent.models import User


@pytest.fixture
def random_user_data(faker):
    random_password = faker.password()
    return {
        "email": faker.email(),
        "password": random_password,
        "password_repeat": random_password,
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
    }


@pytest.mark.django_db
def test_participant_register(random_user_data, api_client):
    participant_register_url = reverse("register-participant")
    response = api_client.post(
        participant_register_url, random_user_data, format="json"
    )
    assert response.status_code == status.HTTP_201_CREATED

    user = User.objects.get(email=random_user_data["email"])
    assert user.groups.all().count() == 1
    assert user.groups.first().id == PARTICIPANT_GROUP_ID


@pytest.mark.django_db
def test_creator_register(random_user_data, api_client):
    participant_register_url = reverse("register-creator")
    response = api_client.post(
        participant_register_url, random_user_data, format="json"
    )
    assert response.status_code == status.HTTP_201_CREATED

    user = User.objects.get(email=random_user_data["email"])
    assert user.groups.all().count() == 1
    assert user.groups.first().id == CREATOR_GROUP_ID
