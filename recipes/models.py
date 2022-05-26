from distutils.command.upload import upload
from turtle import title

from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=164)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=64)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=64)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to='recipes/covers/%Y/%m/%d/', blank=True, default='')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, default=None)

    def __str__(self):
        return self.title
