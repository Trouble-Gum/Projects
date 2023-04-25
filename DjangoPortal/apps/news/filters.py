import django_filters as df
from django_filters import FilterSet
from django_filters import DateTimeFromToRangeFilter
from django_filters.widgets import RangeWidget
# from apps.news.models import Post


class PostFilter(FilterSet):
    date_range = DateTimeFromToRangeFilter(field_name='posted_at',
                                           widget=RangeWidget(attrs={'type': 'datetime-local'}),
                                           lookup_expr='in',
                                           label='Post date'
                                           )
    author_name = df.CharFilter(field_name='author__user__username', lookup_expr='icontains', label='Author')
    caption = df.CharFilter(field_name='caption', lookup_expr='icontains', label='Caption')
    # class Meta:
    #     model = Post
    #     fields = {
    #     }
