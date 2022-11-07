from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
import datetime

User = get_user_model()


class Level(models.Model):
    level = models.CharField(max_length=100)

    def __str__(self):
        return self.level


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(default='', max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


@receiver(pre_save, sender=Category)
def category_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


class Course(models.Model):
    STATUS = (
        ('PUBLISH', 'publish'),
        ('DRAFT', 'draft'),
    )

    owner = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='products', null=True)
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='categories', null=True)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, related_name='levels', null=True)
    description = models.TextField(blank=True)
    status = models.CharField(choices=STATUS, max_length=100, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=100)
    image = models.ImageField(upload_to='images', null=True)
    slug = models.SlugField(default='', max_length=100, null=True, blank=True)
    date = models.DateField(default=datetime.date.today)
    certificate = models.BooleanField(default=False)

    def __str__(self):
        return self.title


@receiver(pre_save, sender=Course)
def category_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


class WhatYouLearn(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='what_learn')
    points = models.CharField(max_length=500) # Раздел для списков, что мы будем изучать

    def __str__(self):
        return self.points


class Requirements(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='requirements')
    points = models.CharField(max_length=500) # Раздел для списков рекомендаций

    def __str__(self):
        return self.points


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lesson')
    title = models.CharField(max_length=500)

    def __str__(self):
        return f'{self.title} - {self.course}'


class Video(models.Model):
    serial_number = models.IntegerField(null=True)
    thumbnail = models.ImageField(upload_to='images', null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson')
    title = models.CharField(max_length=200)
    video = models.URLField(max_length=200)
    time_duration = models.FloatField(null=True)
    preview = models.BooleanField(default=False)

    def __str__(self):
        return self.title




