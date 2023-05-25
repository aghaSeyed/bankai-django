from django.urls import path

from interview.views import AssignmentView

app_name = "interview"
urlpatterns = [
    path("task/<int:pk>/", AssignmentView.as_view(), name="assignment"),
]
