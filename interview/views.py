from django.utils.baseconv import base64
from rest_framework.permissions import AllowAny
from interview.models import Assignment, AssignmentGrade
from interview.serializers import AssignmentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SubmissionSerializer
from .models import TaskQuestion
from question.models import Constraint, TestCase, Language
import requests
import base64


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
            question_task = TaskQuestion.objects.get(id=serializer.data['problem_id'])
            question = question_task.question

            try:
                constraint = Constraint.objects.get(question=question, language_id=serializer.data['language_id'])
            except Constraint.DoesNotExist:
                constraint = None

            test_cases = TestCase.objects.filter(question=question)
            test_case_count = len(test_cases)

            if not test_case_count:
                return Response({'status': "No Test Case have been defined"}, status=status.HTTP_200_OK)

            score = 0
            each_test_score = None if test_case_count == 0 else question_task.score // test_case_count

            for case in test_cases:
                message = case.input
                message_bytes = message.encode('ascii')
                base64_bytes = base64.b64encode(message_bytes)
                base64_input = base64_bytes.decode('ascii')

                message = case.expected_result
                message_bytes = message.encode('ascii')
                base64_bytes = base64.b64encode(message_bytes)
                base64_output = base64_bytes.decode('ascii')

                request_body = {
                    'source_code': serializer.data['code'],
                    'language_id': serializer.data['language_id'],
                    'stdin': base64_input,
                    'compiler_options': "",
                    'command_line_arguments': '',
                    'redirect_stderr_to_stdout': True,
                    'expected_output': base64_output,
                    'cpu_time_limit': constraint.time_limit if constraint else 2,
                    'memory_limit': constraint.memory_limit if constraint else 2048,
                    'max_file_size': constraint.disk_limit if constraint else 3000
                }

                print(request_body)

                response = requests.post(self.url, json=request_body).json()
                print(response)
                if response['status']['id'] == 3:
                    score += each_test_score

            assignment = Assignment.objects.get(task=question_task.task)

            try:
                assignment_grade = AssignmentGrade.objects.get(question=question, assignment=assignment)
                is_higher = assignment_grade.grade < score

                if is_higher:
                    assignment_grade.grade = score
                    assignment_grade.submitted_code = serializer.data['code']

                assignment_grade.submit_count = assignment_grade.submit_count + 1
            except AssignmentGrade.DoesNotExist:
                assignment_grade = AssignmentGrade()
                assignment_grade.assignment = assignment
                assignment_grade.question = question
                assignment_grade.grade = score
                assignment_grade.submit_count = 1
                assignment_grade.submitted_code = serializer.data['code']


            return Response(data={"status": score}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
