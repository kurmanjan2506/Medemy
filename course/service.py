from django_filters import rest_framework as filters
from course.models import Course


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class CourseFilter(filters.FilterSet):
    category = CharFilterInFilter(field_name='category', lookup_expr='in')
    title = CharFilterInFilter(field_name='title', lookup_expr='in')
    owner = CharFilterInFilter(field_name='owner', lookup_expr='in')
    level = CharFilterInFilter(field_name='level', lookup_expr='in')
    price = filters.RangeFilter()

    class Meta:
        model = Course
        fields = ['owner', 'title', 'category', 'price', 'level']