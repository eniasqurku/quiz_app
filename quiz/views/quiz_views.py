from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

from quiz.filters.quiz_filters import QuizFilter
from quiz.serializers.quiz_serializers import (
    QuizReadSerializer,
    QuizWriteSerializer,
    QuizResultSerializer,
)
from quiz.models import Quiz
from quiz_app.common.api_permissions import IsCreator
from quiz_app.common.api_views import (
    MyListCreateAPIView,
    MyRetrieveUpdateDestroyAPIView,
)
from quiz_app.common.utils import is_creator


class QuizListCreateAPIView(MyListCreateAPIView):
    read_serializer_class = QuizReadSerializer
    write_serializer_class = QuizWriteSerializer
    filterset_class = QuizFilter

    def get_queryset(self):
        queryset = Quiz.objects.filter(
            Q(owner=self.request.user)
            | Q(attempted_quizzes__participant=self.request.user)
        )

        return queryset

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsCreator]
        else:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()

    def get_serializer_class(self):
        if not is_creator(self.request.user):
            return QuizResultSerializer

        return super().get_serializer_class()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if not is_creator(self.request.user):
            context["participant"] = self.request.user

        return context


class QuizRetrieveUpdateDestroyView(MyRetrieveUpdateDestroyAPIView):
    write_serializer_class = QuizWriteSerializer
    read_serializer_class = QuizReadSerializer
    lookup_url_kwarg = "quiz_id"

    def get_queryset(self):
        queryset = Quiz.objects.filter(
            Q(owner=self.request.user)
            | Q(attempted_quizzes__participant=self.request.user)
        )

        return queryset

    def get_permissions(self):
        if self.request.method in ["GET"]:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsCreator]

        return super().get_permissions()

    def get_serializer_class(self):
        if not is_creator(self.request.user):
            return QuizResultSerializer

        return super().get_serializer_class()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if not is_creator(self.request.user):
            context["participant"] = self.request.user

        return context
