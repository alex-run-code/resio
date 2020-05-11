import django_filters
from .models import Candidate


class RankingFilter(django_filters.FilterSet):
    class Meta:
        model = Candidate
        fields = ['choice', 'location', 'year']
