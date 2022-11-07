from rest_framework import serializers
from course.serializers import CourseListSerializer
from .models import Review, Like


class ReviewSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    course = serializers.ReadOnlyField(source='course.title')

    class Meta:
        model = Review
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = ('owner', 'review')
