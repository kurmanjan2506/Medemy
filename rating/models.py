from django.db import models
import course.models
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()


class Mark:
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    marks = ((one, 'Ужасно'), (two, 'Плохо'), (three, 'Нормально'), (four, 'Хорошо'), (five, 'Отлично!'))


class Review(models.Model):
    course = models.ForeignKey(course.models.Course, on_delete=models.CASCADE, related_name='reviews')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=Mark.marks)
    text = models.TextField(blank=True)
    created_at = models.DateField(default=datetime.date.today)


class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ['owner', 'review']


class Favorite(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    course = models.ForeignKey(course.models.Course, on_delete=models.CASCADE, related_name='favorites')

    class Meta:
        unique_together = ['owner', 'course']


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commentss')
    course = models.ForeignKey(course.models.Course, on_delete=models.CASCADE, related_name='commentss')
    text = models.TextField()