from course.models import Course
from rest_framework import permissions
from django.shortcuts import get_object_or_404


class IsCourseAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            course_id = int(request.data['course'])
            owner = get_object_or_404(Course, id=course_id).owner
            return request.user == owner
        except:
            return False


class IsCourseAuthorTwo(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(request.user, obj.owner)
        return request.user == obj.owner





