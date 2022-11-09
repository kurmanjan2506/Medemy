from django.contrib import admin
from buy_course.models import UsersCourse


# admin.site.register(UsersCourse)
@admin.register(UsersCourse)
class UsersCourse(admin.ModelAdmin):
    list_display = ('buyer', 'course')