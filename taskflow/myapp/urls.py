from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("user/", views.get_user_data, name="user"),
    path("protected/", views.protected_route, name="protected"),
]
