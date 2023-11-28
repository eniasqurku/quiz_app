import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework import status


@pytest.mark.django_db
def test_creator_cant_notify_about_quizzes_that_dont_belong_to_him(
    api_client, creator_user, quizzes
):
    user = baker.make("agent.User")
    url = reverse("notify", args=[user.id])

    response = api_client.post(url, data={"quiz": quizzes[0].id})
    assert response.status_code == status.HTTP_403_FORBIDDEN
