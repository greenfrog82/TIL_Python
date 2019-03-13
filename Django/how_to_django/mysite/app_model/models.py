from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=120)
    is_active = models.BooleanField(default=True)

    subcategories = models.ManyToManyField('self', symmetrical=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=120)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class City(models.Model):
    name = models.CharField(max_length=120)


class Person(models.Model):
    name = models.CharField(max_length=120)
    hometown = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )


class Book(models.Model):
    name = models.CharField(max_length=120)
    author = models.ForeignKey(
        Person, 
        on_delete=models.CASCADE)