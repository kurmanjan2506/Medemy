# Generated by Django 3.2.16 on 2022-11-07 11:18

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('buy_course', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userscourse',
            name='buyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userscourse',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
