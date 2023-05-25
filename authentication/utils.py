from django.contrib.auth.models import User
from rest_framework.response import Response


def register_user(data):
    user = User()
    user.first_name = data['firstname']
    user.last_name = data['lastname']
    user.email = data['email']
    user.username = data['username']
    user.set_password(data['password'])
    try:
        user.save()
    except Exception as e:
        a = e.args
        return Response({"error": e.args[0]})
    return user
