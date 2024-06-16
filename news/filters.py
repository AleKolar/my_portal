from django_filters import FilterSet, DateFilter, CharFilter
from django.forms import DateInput

from .models import Post


class PostFilter(FilterSet):
    date = DateFilter(
        field_name='created_at',
        label='Дата (позже)',
        lookup_expr='gt',
        widget=DateInput(
            attrs={
                'type': 'date',
            }
        ),
    )
    title = CharFilter(
        field_name='title',
        label='Название',
        lookup_expr='icontains',
    )
    author = CharFilter(
        field_name='authorname',
        label='Автор',
        lookup_expr='icontains',
    )

    class Meta:
        model = Post
        fields = [
            'created_at',
            'title',
            'authorname']
# class PostFilter(FilterSet):
#    class Meta:
#
#        model = Post
#
#        fields = {
#            'title': ['icontains'],
#            'authorname': ['icontains'],
#            'created_at': ['gt'],
#
#        }



