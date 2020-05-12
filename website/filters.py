import django_filters
from .models import Candidate


class RankingFilter(django_filters.FilterSet):
    '''Used to generate filters for the table in the ranking page.'''
    class Meta:
        model = Candidate
        fields = ['choice', 'location', 'year']
