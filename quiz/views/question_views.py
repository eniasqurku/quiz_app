from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from quiz.filters.question_filters import QuestionFilter
from quiz.serializers.question_serializers import (
    QuestionSerializer,
    QuestionSimpleSerializer,
)
from quiz.models import Question
from quiz_app.common.api_permissions import IsCreator
from quiz_app.common.api_views import (
    MyListCreateAPIView,
    MyRetrieveUpdateDestroyAPIView,
)


class QuestionListCreateAPIView(MyListCreateAPIView):
    write_serializer_class = QuestionSerializer
    read_serializer_class = QuestionSimpleSerializer
    filterset_class = QuestionFilter

    def get_queryset(self):
        queryset = Question.objects.filter(
            quiz__owner=self.request.user, quiz_id=self.kwargs["quiz_id"]
        )

        return queryset

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsCreator]
        else:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()


class QuestionRetrieveUpdateDestroyView(MyRetrieveUpdateDestroyAPIView):
    write_serializer_class = QuestionSerializer
    read_serializer_class = QuestionSimpleSerializer
    lookup_url_kwarg = "question_id"

    def get_queryset(self):
        queryset = Question.objects.filter(
            quiz__owner=self.request.user, quiz_id=self.kwargs["quiz_id"]
        )

        return queryset

    def get_permissions(self):
        if self.request.method in ["GET"]:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsCreator]

        return super().get_permissions()
