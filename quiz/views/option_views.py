from quiz.filters.option_filter import OptionFilter
from quiz.models import Option
from quiz.serializers.option_serializer import OptionSerializer
from quiz_app.common.api_permissions import IsCreator
from quiz_app.common.api_views import (
    MyListCreateAPIView,
    MyRetrieveUpdateDestroyAPIView,
)


class OptionListCreateAPIView(MyListCreateAPIView):
    write_serializer_class = OptionSerializer
    read_serializer_class = OptionSerializer
    permission_classes = [IsCreator]
    filterset_class = OptionFilter

    def get_queryset(self):
        question_id = self.kwargs["question_id"]
        queryset = Option.objects.filter(
            question__quiz__owner=self.request.user, question_id=question_id
        )

        return queryset


class OptionRetrieveUpdateDestroyView(MyRetrieveUpdateDestroyAPIView):
    write_serializer_class = OptionSerializer
    read_serializer_class = OptionSerializer
    permission_classes = [IsCreator]
    lookup_url_kwarg = "option_id"

    def get_queryset(self):
        question_id = self.kwargs["question_id"]
        queryset = Option.objects.filter(
            question__quiz__owner=self.request.user, question_id=question_id
        )

        return queryset
