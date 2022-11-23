from django_filters import rest_framework as filters

from agent.models import User
from quiz.models import Quiz


class UserFilter(filters.FilterSet):
    first_name = filters.CharFilter(lookup_expr='icontains')
    last_name = filters.CharFilter(lookup_expr='icontains')
    email = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['id']
