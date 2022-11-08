from rest_framework import serializers
from django.db.models import Avg

from . import models
from .models import Category, Course, WhatYouLearn, Requirements, Lesson, Video, Level


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


class CourseListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    category = serializers.PrimaryKeyRelatedField(required=True, queryset=Category.objects.all())

    class Meta:
        model = Course
        fields = ('id', 'owner', 'title', 'price', 'image', 'category', 'description')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['rating'] = instance.reviews.aggregate(Avg('rating'))['rating__avg']
        repr['rating_count'] = instance.reviews.count()
        return repr


class CourseDetailSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    category = serializers.PrimaryKeyRelatedField(required=True, queryset=Category.objects.all())

    class Meta:
        model = Course
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['rating'] = instance.reviews.aggregate(Avg('rating'))['rating__avg']
        repr['rating_count'] = instance.reviews.count()
        repr['favorites_count'] = instance.favorites.count()
        return repr


class WhatYouLearnSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), required=True)

    class Meta:
        model = WhatYouLearn
        fields = '__all__'

    def create(self, validated_data):
        return WhatYouLearn.objects.create(**validated_data)


class RequirementsSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), required=True)

    class Meta:
        model = Requirements
        fields = '__all__'

    def create(self, validated_data):
        return Requirements.objects.create(**validated_data)


class LessonSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), required=True)

    class Meta:
        model = Lesson
        fields = '__all__'

    def create(self, validated_data):
        return Lesson.objects.create(**validated_data)


class VideoSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), required=True)

    class Meta:
        model = Video
        fields = '__all__'

    def create(self, validated_data):
        return Video.objects.create(**validated_data)