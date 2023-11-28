import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework import status


@pytest.mark.django_db
def test_user_participation(api_client, participant_user):
    participation_url = reverse("quiz-attempts")
    quiz = baker.make("quiz.Quiz")

    response = api_client.post(participation_url, data={"quiz": quiz.id})
    assert response.status_code == status.HTTP_201_CREATED
    assert participant_user.attempted_quizzes.first().quiz == quiz


@pytest.mark.django_db
def test_user_participating_twice_in_a_quiz(api_client, participant_user):
    participation_url = reverse("quiz-attempts")
    quiz = baker.make("quiz.Quiz")

    response = api_client.post(participation_url, data={"quiz": quiz.id})
    assert response.status_code == status.HTTP_201_CREATED

    response = api_client.post(participation_url, data={"quiz": quiz.id})
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
