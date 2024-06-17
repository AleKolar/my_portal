from django_filters import FilterSet, DateFilter, CharFilter, ChoiceFilter
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

    post_type = ChoiceFilter(
        field_name='post_type',
        label='Тип поста',
        choices=Post.POST_TYPES,
    )

    class Meta:
        model = Post
        fields = [
            'date',
            'title',
            'author',
            'post_type',
        ]
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



