from django.db import models
from django.contrib.auth.models import User

from bankai.models import BaseModel


class Category(BaseModel):
    title = models.CharField(max_length=50)


class Question(BaseModel):
    title = models.CharField(max_length=50)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='questions')
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name='questions')


class TestCase(models.Model):
    input = models.TextField()
    expected_result = models.TextField()
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='test_cases')


class Language(models.Model):
    name = models.CharField(blank=True, null=True)
    judge = models.IntegerField(blank=False, null=False)


class Constraint(models.Model):
    time_limit = models.IntegerField()
    memory_limit = models.IntegerField()
    disk_limit = models.IntegerField()
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='constraints')
    language = models.ForeignKey('Language', on_delete=models.CASCADE, related_name='constraints')
