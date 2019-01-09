from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Author(models.Model):
    name = models.CharField(max_length=100)
    
class Article(models.Model):
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)

    author = models.ForeignKey(Author, related_name='articles', on_delete=models.CASCADE, null=True)

    # def save(self, **kwargs):
    #     import pdb; pdb.set_trace()
    #     super(Point, self).save(**kwargs)

class Point(models.Model):
    x = models.PositiveIntegerField()
    y = models.PositiveIntegerField()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=10)
    platform_id = models.CharField(max_length=10)

    class Meta:
        unique_together = ('user', 'platform', 'platform_id')


class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    try_to_travel = models.BooleanField(null=True)


class MyPerson(Person):
    class Meta:
        proxy = True


class OrderedPerson(Person):
    class Meta:
        ordering = ['-last_name']
        proxy = True


class Group(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class Part(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class Member(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

# class Manager(models.Model):
#     group = models.OneToOneField(Group, related_name='manager', null=True)
#     franchise = models.OneToOneField(Franchises, related_name='manager', null=True)
#     restaurant = models.OneToOneField(Restaurant, related_name='manager', null=True)

class Manager(models.Model):
    group = models.PositiveIntegerField(null=True)
    part = models.PositiveIntegerField(null=True)
    member = models.PositiveIntegerField(null=True)
 
    class Meta:
        unique_together = ('group', 'part', 'member')
    

class DateTimeTestModel(models.Model):
    created_at_1 = models.DateTimeField(auto_now_add=True)
    created_at_2 = models.DateTimeField(default=timezone.now)
    created_at_3 = models.DateTimeField(default=datetime.now)

