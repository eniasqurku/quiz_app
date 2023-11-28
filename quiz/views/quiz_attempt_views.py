from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

from quiz.filters.quiz_attempt_filter import QuizAttemptFilter
from quiz.models import QuizAttempt
from quiz.serializers.quiz_attempt_serializers import (
    QuizAttemptWriteSerializer,
    QuizAttemptReadSerializer,
)
from quiz_app.common.api_permissions import IsParticipant
from quiz_app.common.api_views import (
    MyListCreateAPIView,
)


class QuizAttemptListCreateAPIView(MyListCreateAPIView):
    write_serializer_class = QuizAttemptWriteSerializer
    read_serializer_class = QuizAttemptReadSerializer
    filterset_class = QuizAttemptFilter

    def get_queryset(self):
        user = self.request.user
        return QuizAttempt.objects.filter(Q(participant=user) | Q(quiz__owner=user))

    def get_permissions(self):
        if self.request.method in ["POST"]:
            self.permission_classes = [IsParticipant]
        else:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()
