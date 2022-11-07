from django.contrib import admin
from .models import Review, Like

admin.site.register(Like)


@admin.register(Review)
class Review(admin.ModelAdmin):
    list_display = ('owner', 'course', 'rating', 'created_at')
