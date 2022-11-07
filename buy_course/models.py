from django.db import models
from django.contrib.auth import get_user_model
from course.models import Course
import datetime

User = get_user_model()


class UsersCourse(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='buy_course')
    paid = models.BooleanField(default=0)
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f'{self.buyer} - {self.course.title}'


