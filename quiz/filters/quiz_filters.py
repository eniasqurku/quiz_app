from django_filters import rest_framework as filters

from quiz.models import Quiz


class QuizFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr="icontains")
    question = filters.CharFilter(
        field_name="questions__title", lookup_expr="icontains"
    )

    class Meta:
        model = Quiz
        fields = ["id"]
