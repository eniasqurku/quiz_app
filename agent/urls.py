from django.urls import path

from agent.views.agent_class_views import (
    ParticipantListAPIView,
    UserQuizzesListAPIView,
    UserQuizzesRetrieveAPIView,
)
from agent.views.agent_function_views import notify, invite_participant

urlpatterns = [
    path("participants/", ParticipantListAPIView.as_view(), name="participants"),
    path(
        "participants/<int:user_id>/quizzes/",
        UserQuizzesListAPIView.as_view(),
        name="user-quizzes",
    ),
    path(
        "participants/<int:user_id>/quizzes/<int:pk>/",
        UserQuizzesRetrieveAPIView.as_view(),
        name="user-quiz",
    ),
    path("participants/<int:pk>/notify/", notify, name="notify"),
    path("invite/", invite_participant, name="invite"),
]
