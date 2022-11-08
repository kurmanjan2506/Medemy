from django.db import models
from datetime import datetime


class Room(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.TimeField(auto_now_add=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)





