from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, response
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rating.serializers import ReviewSerializer
from .models import Course, Category, WhatYouLearn, Requirements, Lesson, Video, Level
from . import serializers
from rest_framework.pagination import PageNumberPagination

from .permissions import IsCourseAuthor
from .serializers import WhatYouLearnSerializer, RequirementsSerializer
from rest_framework.decorators import action
from rating.models import Favorite


class StandartResultPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    max_page_size = 1000


class CategoryViewSet(ModelViewSet):
    serializer_class = serializers.CategorySerializer
    pagination_class = StandartResultPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    queryset = Category.objects.all()
    search_fields = ['title']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class LevelViewSet(ModelViewSet):
    serializer_class = serializers.LevelSerializer
    pagination_class = StandartResultPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    queryset = Level.objects.all()
    search_fields = ['title']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = StandartResultPagination
    search_fields = ['title']
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_fields = ('owner', 'category', 'price')

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [IsCourseAuthor()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.CourseListSerializer
        return serializers.CourseDetailSerializer

    # api/v1/courses/<id>/reviews/
    @action(['GET', 'POST'], detail=True)
    def reviews(self, request, pk):
        course = self.get_object()
        if request.method == 'GET':
            reviews = course.reviews.all()
            serializer = ReviewSerializer(reviews, many=True)
            return response.Response(serializer.data, status=200)
        if course.reviews.filter(owner=request.user).exists():
            return response.Response('Вы уже оставляли отзыв!', status=400)
        data = request.data
        serializer = ReviewSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user, course=course)
        return response.Response(serializer.data, status=201)

    @action(['POST'], detail=True)
    def favorite_action(self, request, pk):
        course = self.get_object()
        user = request.user
        if user.favorites.filter(course=course).exists():
            user.favorites.filter(course=course).delete()
            return Response('Deleted From Favorites!', status=204)
        Favorite.objects.create(owner=user, course=course)
        return Response('Added to Favorites!', status=201)


class WhatYouLearnViewSet(ModelViewSet):
    queryset = WhatYouLearn.objects.all()
    serializer_class = serializers.WhatYouLearnSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [IsCourseAuthor()]


class RequirementsViewSet(ModelViewSet):
    queryset = Requirements.objects.all()
    serializer_class = serializers.RequirementsSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [IsCourseAuthor()]


class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = serializers.LessonSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [IsCourseAuthor()]


class VideoViewSet(ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = serializers.VideoSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [IsCourseAuthor()]


# TODO search
