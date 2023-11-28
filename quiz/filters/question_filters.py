from django_filters import rest_framework as filters

from quiz.models import Question


class QuestionFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Question
        fields = ["id"]
