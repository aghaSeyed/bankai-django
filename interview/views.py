from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from interview.models import Assignment
from interview.serializers import AssignmentSerializer


class AssignmentView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        assignment = Assignment.objects.get(pk=pk)

        return Response(
            AssignmentSerializer(assignment).data
        )
