from django_filters import rest_framework as filters

from quiz.models import Option


class OptionFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Option
        fields = ["id", "title", "correct"]
