from django_filters import rest_framework as filters

from quiz.models import QuizAttempt


class QuizAttemptFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="quiz__title", lookup_expr="icontains")
    email = filters.CharFilter(field_name="participant__email", lookup_expr="icontains")
    first_name = filters.CharFilter(
        field_name="participant__first_name", lookup_expr="icontains"
    )
    last_name = filters.CharFilter(
        field_name="participant__last_name", lookup_expr="icontains"
    )

    class Meta:
        model = QuizAttempt
        fields = ["id", "participant", "quiz"]
