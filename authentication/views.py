from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializers import RegisterSerializer, UserIdSerializer
from authentication.utils import register_user
from bankai.commonResponses import invalidDataResponse
from bankai.commonScemas import invalid_data_schema


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={
            201: UserIdSerializer,
            406: invalid_data_schema(),
        },
    )
    def post(self, request):
        post_data = request.data
        serializer = RegisterSerializer(data=post_data)

        if not serializer.is_valid():
            return invalidDataResponse()

        response = register_user(serializer.data)
        if isinstance(response, User):
            return Response(
                UserIdSerializer(response).data,
                status=status.HTTP_201_CREATED
            )

        return response
