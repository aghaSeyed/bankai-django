from django.contrib.auth.models import User
from django.db import models
from bankai.models import BaseModel


class Task(BaseModel):
    title = models.CharField(max_length=300)
    description = models.TextField()
    duration = models.IntegerField()
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="tasks", null=False, blank=False
    )


class Assignment(BaseModel):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='assignments', null=False, blank=False
    )
    email = models.EmailField(null=False)
    expiration_date = models.DateTimeField()


class TaskQuestion(BaseModel):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='task_questions', null=False, blank=False
    )
    question = models.ForeignKey(
        'question.models.Question', on_delete=models.CASCADE, related_name='task_questions', null=False, blank=False
    )
    score = models.IntegerField(null=False)


class AssignmentGrade(BaseModel):
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, related_name='assignment_grades', null=False, blank=False
    )
    question = models.ForeignKey(
        'question.models.Question', on_delete=models.CASCADE, related_name='assignment_grades', null=False, blank=False
    )
    grade = models.IntegerField(null=False)
