from django_filters import rest_framework as filters

from quiz.models import Question


class QuestionFilter(filters.FilterSet):
    quiz_title = filters.CharFilter(field_name='quiz__title', lookup_expr='icontains')
    title = filters.CharFilter(lookup_expr='icontains')
    option_1 = filters.CharFilter(lookup_expr='icontains')
    option_2 = filters.CharFilter(lookup_expr='icontains')
    option_3 = filters.CharFilter(lookup_expr='icontains')
    option_4 = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Question
        fields = ["id", "correct_answer", "quiz"]
