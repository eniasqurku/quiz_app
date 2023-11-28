from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from quiz.filters.answer_filter import AnswerFilter
from quiz.serializers.answer_serializers import (
    AnswerWriteSerializer,
    AnswerReadSerializer,
)
from quiz.models import ParticipantAnswer
from quiz_app.common.api_permissions import CanDelete, IsParticipant
from quiz_app.common.api_views import (
    MyListCreateAPIView,
    MyRetrieveUpdateDestroyAPIView,
)
from quiz_app.cons import MESSAGE


class AnswerListCreateAPIView(MyListCreateAPIView):
    write_serializer_class = AnswerWriteSerializer
    read_serializer_class = AnswerReadSerializer
    filterset_class = AnswerFilter
    permission_classes = [IsParticipant]

    def get_queryset(self):
        queryset = ParticipantAnswer.objects.filter(participant=self.request.user)

        return queryset


class AnswerRetrieveUpdateDestroyView(MyRetrieveUpdateDestroyAPIView):
    write_serializer_class = AnswerWriteSerializer
    read_serializer_class = AnswerReadSerializer
    permission_classes = [IsParticipant]

    def get_queryset(self):
        queryset = ParticipantAnswer.objects.filter(participant=self.request.user)

        return queryset

    def delete(self, request, *args, **kwargs):
        return Response(
            {MESSAGE: "Cannot delete answers"}, status=status.HTTP_204_NO_CONTENT
        )
