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

