from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.


class User(AbstractUser):
    # username = models.CharField(max_length=100)
    email = models.EmailField(max_length=30)
    # age = models.PositiveIntegerField()
    # password = models.CharField(max_length=30)

    def __str__(self):
        return self.username


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    ingredients = models.TextField(blank=True)
    instructions = models.TextField(blank=True)
    image = models.ImageField(upload_to='recipes/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recipe')
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='favourite_recipes', blank=True)

    def __str__(self):
        return self.title
