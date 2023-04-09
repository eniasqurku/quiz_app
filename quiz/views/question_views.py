from quiz.filters.question_filters import QuestionFilter
from quiz.model_serializers.question_serializers import QuestionSerializer
from quiz.models import Question
from quiz_app.common.api_permissions import IsCreator
from quiz_app.common.api_views import MyListCreateAPIView, MyRetrieveUpdateDestroyAPIView


class QuestionListCreateAPIView(MyListCreateAPIView):
    queryset = Question.objects.all()
    write_serializer_class = QuestionSerializer
    read_serializer_class = QuestionSerializer
    permission_classes = [IsCreator]
    filterset_class = QuestionFilter

    def get_queryset(self):
        queryset = Question.objects.filter(quiz__owner=self.request.user)

        return queryset


class QuestionRetrieveUpdateDestroyView(MyRetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    write_serializer_class = QuestionSerializer
    read_serializer_class = QuestionSerializer
    permission_classes = [IsCreator]

    def get_queryset(self):
        queryset = Question.objects.filter(quiz__owner=self.request.user)

        return queryset
