from django.urls import path

from agent.model_views.agent_views import ParticipantListAPIView, invite_participant, UserQuizzes, MyQuizzes, notify

urlpatterns = [
    path('participants/', ParticipantListAPIView.as_view(), name='participants'),
    path('participants/<int:pk>/quizzes/', UserQuizzes.as_view(), name='user-quizzes'),
    path('participants/<int:pk>/notify/', notify, name='notify'),
    path('participants/my/quizzes/', MyQuizzes.as_view(), name='my-quizzes'),
    path('invite/', invite_participant, name='invite'),
]
