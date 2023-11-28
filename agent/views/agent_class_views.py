from rest_framework.generics import get_object_or_404, RetrieveAPIView

from agent.filters.agent_filters import UserFilter
from agent.models import User
from agent.serializers.agent_serializers import (
    UserReadSerializer,
)
from quiz.filters.quiz_filters import QuizFilter
from quiz.models import Quiz
from quiz.serializers.quiz_serializers import QuizResultSerializer
from quiz_app.common.api_permissions import IsCreator
from quiz_app.common.api_views import MyListAPIView


class ParticipantListAPIView(MyListAPIView):
    serializer_class = UserReadSerializer
    filterset_class = UserFilter
    permission_classes = [IsCreator]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(attempted_quizzes__quiz__in=user.quizzes.all())


class UserQuizzesListAPIView(MyListAPIView):
    serializer_class = QuizResultSerializer
    filterset_class = QuizFilter
    permission_classes = [IsCreator]

    def get_queryset(self):
        participant = get_object_or_404(User, pk=self.kwargs["user_id"])

        return Quiz.objects.filter(
            attempted_quizzes__participant=participant, owner=self.request.user
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["participant"] = get_object_or_404(User, pk=self.kwargs["user_id"])

        return context


class UserQuizzesRetrieveAPIView(RetrieveAPIView):
    serializer_class = QuizResultSerializer
    permission_classes = [IsCreator]

    def get_queryset(self):
        participant = get_object_or_404(User, pk=self.kwargs["user_id"])

        return Quiz.objects.filter(
            attempted_quizzes__participant=participant, owner=self.request.user
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["participant"] = get_object_or_404(User, pk=self.kwargs["user_id"])

        return context
