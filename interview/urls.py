from django.urls import path

from interview.views import AssignmentView, SubmissionApiView

app_name = "interview"
urlpatterns = [
    path("task/<int:pk>/", AssignmentView.as_view(), name="assignment"),
    path('api/submit', SubmissionApiView.as_view(), name='submit')
]
