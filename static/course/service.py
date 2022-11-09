from django_filters import rest_framework as filters
from course.models import Course


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class CourseFilter(filters.FilterSet):
    owner = CharFilterInFilter(field_name='owner', lookup_expr='in')
    category = CharFilterInFilter(field_name='category', lookup_expr='in')
    # max_price = CharFilterInFilter(field_name='max_price', lookup_expr='in')
    price = filters.RangeFilter()

    class Meta:
        model = Course
        fields = ['owner', 'category', 'price']