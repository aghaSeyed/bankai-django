from django.contrib import admin

from question.models import Category, Question, Language, Constraint, TestCase

admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Language)
admin.site.register(Constraint)
admin.site.register(TestCase)