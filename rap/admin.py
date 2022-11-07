from django.contrib import admin
from buy_course.models import UsersCourse
from rap.models import CustomUser, Spam_Contacts


class YourCourseTabInline(admin.TabularInline):
    model = UsersCourse


@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    list_display = ('username', 'photo')
    inlines = (YourCourseTabInline,)


admin.site.register(Spam_Contacts)