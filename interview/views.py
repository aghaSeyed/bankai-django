from rest_framework.permissions import AllowAny
from interview.models import Assignment
from interview.serializers import AssignmentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SubmissionSerializer
from .models import TaskQuestion
from question.models import Constraint, TestCase, Language
import requests


class AssignmentView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        assignment = Assignment.objects.get(pk=pk)

        return Response(
            AssignmentSerializer(assignment).data
        )



class SubmissionApiView(APIView):
    url = 'http://139.144.176.22:2358/submissions?base64_encoded=true&wait=true'

    def permission_denied(self, request, message=None, code=None):
        return

    def post(self, request, format=None):
        serializer = SubmissionSerializer(data=request.data)
        if serializer.is_valid():
            question_task = TaskQuestion.objects.get(id=serializer.data['task_question_id'])
            question = question_task.question
            constraint = Constraint.objects.get(question=question, language_id=serializer.data['language_id'])
            language = Language.objects.get()
            test_cases = TestCase.objects.filter(question=question)
            response = []
            for case in test_cases:
                request_body = {
                    'source_code': serializer.data['code'],
                    'language_id': serializer.data['language_id'],
                    'stdin': case.input,
                    'compiler_options': language.compiler_option,
                    'command_line_arguments': '',
                    'redirect_stderr_to_stdout': True,
                    'expected_output': case.expected_result,
                    'cpu_time_limit': constraint.time_limit,
                    'memory_limit': constraint.memory_limit,
                    'max_file_size': constraint.disk_limit
                }

                response.append(requests.post(self.url, json=request_body).json())
            return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
