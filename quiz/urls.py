from django.urls import path

from quiz.views.answer_views import (
    AnswerListCreateAPIView,
    AnswerRetrieveUpdateDestroyView,
)
from quiz.views.option_views import (
    OptionListCreateAPIView,
    OptionRetrieveUpdateDestroyView,
)
from quiz.views.question_views import (
    QuestionListCreateAPIView,
    QuestionRetrieveUpdateDestroyView,
)
from quiz.views.quiz_attempt_views import QuizAttemptListCreateAPIView
from quiz.views.quiz_views import QuizListCreateAPIView, QuizRetrieveUpdateDestroyView

QUIZ_URL_BASE = r"quizzes/<int:quiz_id>"
QUESTION_URL_BASE = r"questions/<int:question_id>"
OPTION_URL_BASE = r"options/<int:option_id>"

urlpatterns = [
    path("quizzes/", QuizListCreateAPIView.as_view(), name="quizzes"),
    path(f"{QUIZ_URL_BASE}/", QuizRetrieveUpdateDestroyView.as_view(), name="quiz"),
    path(
        f"{QUIZ_URL_BASE}/questions/",
        QuestionListCreateAPIView.as_view(),
        name="questions",
    ),
    path(
        f"{QUIZ_URL_BASE}/{QUESTION_URL_BASE}/",
        QuestionRetrieveUpdateDestroyView.as_view(),
        name="question",
    ),
    path(
        f"{QUESTION_URL_BASE}/options/",
        OptionListCreateAPIView.as_view(),
        name="options",
    ),
    path(
        f"{QUESTION_URL_BASE}/{OPTION_URL_BASE}/",
        OptionRetrieveUpdateDestroyView.as_view(),
        name="option",
    ),
    path("answers/", AnswerListCreateAPIView.as_view(), name="answers"),
    path("answers/<int:pk>/", AnswerRetrieveUpdateDestroyView.as_view(), name="answer"),
    path(
        "quiz-attempts/", QuizAttemptListCreateAPIView.as_view(), name="quiz-attempts"
    ),
]
