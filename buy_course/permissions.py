from buy_course.models import UsersCourse
from rest_framework import permissions
from django.shortcuts import get_object_or_404


class IsCourseBuyer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            course_id = int(request.data['course'])
            buyer = get_object_or_404(UsersCourse, id=course_id).buyer
            print(buyer, '!!!!!!!!!!!!!!11')
            return request.user == buyer
        except:
            return False
