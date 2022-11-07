from rest_framework import serializers
from .models import Course
from buy_course.models import UsersCourse


class UsersCourseSerializer(serializers.ModelSerializer):
    buyer = serializers.ReadOnlyField(source='buyer.username')

    class Meta:
        model = UsersCourse
        fields = '__all__'
