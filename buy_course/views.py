from django.http import Http404
from course.models import Course
from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from buy_course.serializers import UsersCourseSerializer
from course.views import StandartResultPagination
from . import serializers
from .models import UsersCourse
from buy_course.permissions import IsCourseBuyer
from .send_email import send_confirmation_email


class UsersCourseView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.AllowAny()]
        return [IsCourseBuyer()]

    def get_object(self, pk):
        try:
            return UsersCourse.objects.get(pk=pk)
        except UsersCourse.DoesNotExist:
            raise Http404

    def get(self, request):
        queryset = UsersCourse.objects.all()
        serializer = serializers.UsersCourseSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = serializers.UsersCourseSerializer(data=request.data)
        course_id = int(request.data['course'])
        # course_title = Course.objects.all()
        course_title = get_object_or_404(Course, id=course_id)
        if request.user.buyer.filter(course=course_id).exists():
            return Response('Вы уже купили этот курс!', 400)

        if serializer.is_valid(raise_exception=True):
            bought = serializer.save(buyer=request.user, paid=True)
            if bought:
                send_confirmation_email(request.user.email, course_title)
            return Response(serializer.data, status=201)

    def delete(self, request, pk):
        # course_id = int(request.data['course'])
        # queryset = UsersCourse.objects.all()
        # if request.user.buyer.filter(course=course_id).exists():
        #     queryset.delete()
        course = self.get_object(pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





