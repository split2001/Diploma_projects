# Generated by Django 5.1.3 on 2024-11-27 14:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='my_favourite',
            field=models.ManyToManyField(related_name='favourite_recipes', to=settings.AUTH_USER_MODEL),
        ),
    ]
