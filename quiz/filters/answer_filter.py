from django_filters import rest_framework as filters

from quiz.models import ParticipantAnswer


class AnswerFilter(filters.FilterSet):
    quiz_title = filters.CharFilter(field_name='question__quiz__title', lookup_expr='icontains')
    quiz = filters.CharFilter(field_name='question__quiz')
    first_name = filters.CharFilter(field_name='participant__first_name', lookup_expr='icontains')
    last_name = filters.CharFilter(field_name='participant__last_name', lookup_expr='icontains')
    email = filters.CharFilter(field_name='participant__email', lookup_expr='icontains')

    class Meta:
        model = ParticipantAnswer
        fields = ["id", "question", 'answer', 'participant']
