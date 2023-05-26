from django.urls import path

from interview.views import AssignmentView, SubmissionApiView

app_name = "interview"
urlpatterns = [
    path("api/tasks/task/<int:pk>/", AssignmentView.as_view(), name="assignment"),
    path('api/judge/submit', SubmissionApiView.as_view(), name='submit')
]
