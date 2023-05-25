from django.urls import path
from .views import RegisterView

app_name = "authentication"
urlpatterns = [
    path("signup", RegisterView.as_view(), name="register"),
]
