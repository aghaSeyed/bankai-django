from django.contrib import admin

from interview.models import Task, Assignment, TaskQuestion, AssignmentGrade

admin.site.register(Task)
admin.site.register(Assignment)
admin.site.register(TaskQuestion)
admin.site.register(AssignmentGrade)
