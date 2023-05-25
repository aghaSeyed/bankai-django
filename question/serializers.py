from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Category, Question


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']

