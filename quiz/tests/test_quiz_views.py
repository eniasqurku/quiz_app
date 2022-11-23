import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from quiz.models import Quiz, TakenQuiz



def create_questions(quiz):
    return baker.make('quiz.Question', quiz=quiz, _quantity=5)


def create_quiz(user):
    return baker.make('quiz.Quiz', owner=user)


def test_creator_can_see_his_quizzes(api_client, creator_user, create_quizzes):
    quizzes_url = reverse('quizzes')
    quiz = create_quiz(creator_user)
    create_questions(quiz)

    response = api_client.get(quizzes_url)

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    for quiz in response_data['data']:
        quiz_id = quiz['id']
        quiz_obj = Quiz.objects.get(id=quiz_id)
        assert quiz_obj.owner == creator_user


def test_participant_cant_create_quizzes(api_client, participant_user):
    quizzes_url = reverse('quizzes')
    response = api_client.post(quizzes_url, data={})

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_participant_cant_see_any_quizzes_without_participating(api_client, participant_user, create_quizzes):
    quizzes_url = reverse('quizzes')
    response = api_client.get(quizzes_url)
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert response_data['data'] == []


def test_participant_can_only_see_quizzes_he_participated(api_client, participant_user, create_quizzes):
    quizzes_url = reverse('quizzes')
    quiz_1 = create_quizzes[0]
    quiz_2 = create_quizzes[1]
    TakenQuiz.objects.create(quiz=quiz_1, participant=participant_user)
    TakenQuiz.objects.create(quiz=quiz_2, participant=participant_user)
    response = api_client.get(quizzes_url)
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert len(response_data['data']) == 2
    for quiz in response_data['data']:
        assert quiz['id'] in [quiz_1.id, quiz_2.id]
