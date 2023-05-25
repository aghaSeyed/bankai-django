from datetime import timedelta

from rest_framework import serializers

from interview.models import Assignment, AssignmentGrade, TaskQuestion
from question.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id',
            'title',
            'description',
        ]


class AnswerSerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField()

    @staticmethod
    def get_score(assignment_grade):
        return assignment_grade.grade

    class Meta:
        model = AssignmentGrade
        fields = [
            'score',
            'submitted_code',
        ]


class QuestionDetailSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()
    answer = serializers.SerializerMethodField()

    @staticmethod
    def get_question(task_question):
        return QuestionSerializer(instance=task_question.question).data

    def get_answer(self, task_question):
        assignment_id = self.context['assignment_id']
        assignment = Assignment.objects.get(pk=assignment_id)
        question = task_question.question

        try:
            assignment_grade = AssignmentGrade.objects.get(assignment=assignment, question=question)
        except AssignmentGrade.DoesNotExist:
            assignment_grade = None

        if not assignment_grade:
            return {
                "score": None,
                "submitted_code": None
            }

        return AnswerSerializer(instance=assignment_grade).data

    class Meta:
        model = TaskQuestion
        fields = [
            'question',
            'answer'
        ]


class AssignmentSerializer(serializers.ModelSerializer):
    question_details = serializers.SerializerMethodField()
    task_id = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    @staticmethod
    def get_task_id(assignment):
        return assignment.id

    @staticmethod
    def get_title(assignment):
        return assignment.task.title

    @staticmethod
    def get_description(assignment):
        return assignment.task.description

    @staticmethod
    def get_end_time(assignment):
        return assignment.start_date + timedelta(seconds=assignment.task.duration)

    @staticmethod
    def get_question_details(assignment):
        task_questions = assignment.task.task_questions

        result = []
        for task_question in task_questions:
            result.append(QuestionDetailSerializer(instance=task_question, context={'assignment_id': assignment.id}))

        return result

    class Meta:
        model = Assignment
        fields = [
            'task_id',
            'title',
            'description',
            'end_time',
            'question_details',
        ]
