from django.contrib import admin
from .models import Category, Course, Level, Requirements, WhatYouLearn, Lesson, Video


class WhatYouLearnTabInline(admin.TabularInline):
    model = WhatYouLearn


class RequirementsTabInline(admin.TabularInline):
    model = Requirements


class LessonTabInline(admin.TabularInline):
    model = Lesson


class VideoTabInline(admin.TabularInline):
    model = Video


class CourseAdmin(admin.ModelAdmin):
    inlines = (WhatYouLearnTabInline, RequirementsTabInline, LessonTabInline, VideoTabInline)


admin.site.register(Level)
admin.site.register(Category)
admin.site.register(Course, CourseAdmin)
admin.site.register(WhatYouLearn)
admin.site.register(Requirements)
# admin.site.register(Lesson)
admin.site.register(Video)


@admin.register(Lesson)
class Lesson(admin.ModelAdmin):
    list_display = ('course', 'title', 'learned')





