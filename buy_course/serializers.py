from rest_framework import serializers
from .models import Course
from buy_course.models import UsersCourse


class UsersCourseSerializer(serializers.ModelSerializer):
    buyer = serializers.ReadOnlyField(source='purchased_courses.username')

    class Meta:
        model = UsersCourse
        fields = '__all__'
