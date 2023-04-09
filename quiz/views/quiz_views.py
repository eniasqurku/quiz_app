from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

from quiz.filters.quiz_filters import QuizFilter
from quiz.model_serializers.quiz_serializers import QuizReadSerializer, QuizWriteSerializer
from quiz.models import Quiz
from quiz_app.common.api_permissions import IsCreator
from quiz_app.common.api_views import MyListCreateAPIView, MyRetrieveUpdateDestroyAPIView


class QuizListCreateAPIView(MyListCreateAPIView):
    read_serializer_class = QuizReadSerializer
    write_serializer_class = QuizWriteSerializer
    filterset_class = QuizFilter

    def get_queryset(self):
        queryset = Quiz.objects.filter(Q(owner=self.request.user) | Q(user_quizzes__participant=self.request.user))

        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsCreator]
        else:
            self.permission_classes = [IsAuthenticated]

        return super(QuizListCreateAPIView, self).get_permissions()


class QuizRetrieveUpdateDestroyView(MyRetrieveUpdateDestroyAPIView):
    write_serializer_class = QuizWriteSerializer
    read_serializer_class = QuizReadSerializer

    def get_queryset(self):
        queryset = Quiz.objects.filter(Q(owner=self.request.user) | Q(user_quizzes__participant=self.request.user))

        return queryset

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            self.permission_classes = [IsCreator]
        else:
            self.permission_classes = [IsAuthenticated]

        return super(QuizRetrieveUpdateDestroyView, self).get_permissions()
