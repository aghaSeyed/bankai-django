from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    firstname = serializers.CharField(max_length=200)
    lastname = serializers.CharField(max_length=200)
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)
    email = serializers.EmailField()


class UserIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']
