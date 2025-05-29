from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Authentication endpoints
    path("register/", views.RegisterView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # User endpoints
    path("user/", views.UserDetailView.as_view(), name="user-detail"),
    path("users/", views.UserListView.as_view(), name="user-list"),
    # Task endpoints
    path("tasks/", views.TaskListCreateView.as_view(), name="task-list-create"),
    path("tasks/<int:id>/", views.TaskDetailView.as_view(), name="task-detail"),
    path(
        "tasks/<int:task_id>/status/",
        views.update_task_status,
        name="update-task-status",
    ),
    # Admin deletion endpoints
    path(
        "admin/users/<int:user_id>/delete/",
        views.admin_delete_user,
        name="admin-delete-user",
    ),
    path(
        "admin/tasks/<int:task_id>/delete/",
        views.admin_delete_task,
        name="admin-delete-task",
    ),
    path("admin/bulk-delete/", views.admin_bulk_delete, name="admin-bulk-delete"),
]
