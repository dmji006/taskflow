from django.shortcuts import render, get_object_or_404
from django.http import Http404
from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Q
from .models import User, Task
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    TaskSerializer,
)
from .utils import rate_limit


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    @rate_limit(requests=5, interval=60)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["username", "email", "first_name", "last_name"]
    ordering_fields = ["username", "date_joined"]
    ordering = ["username"]

    def get_queryset(self):
        return User.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"count": queryset.count(), "results": serializer.data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_data(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def protected_route(request):
    return Response(
        {
            "message": "You have access to this protected route",
            "user": request.user.username,
        }
    )


class UserDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


# Task Views
class TaskListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "updated_at", "priority", "status"]
    ordering = ["-created_at"]

    @rate_limit(requests=5, interval=60)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    @rate_limit(requests=5, interval=60)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_staff:  # Admin users can see all tasks
            queryset = Task.objects.all()
        else:  # Regular users can only see their tasks
            queryset = Task.objects.filter(created_by=self.request.user)

        # Apply filters
        if queryset.exists():
            status = self.request.query_params.get("status", None)
            if status:
                queryset = queryset.filter(status=status)

            priority = self.request.query_params.get("priority", None)
            if priority:
                queryset = queryset.filter(priority=priority)

            created_by = self.request.query_params.get("created_by", None)
            if (
                created_by and self.request.user.is_staff
            ):  # Only admins can filter by created_by
                queryset = queryset.filter(created_by_id=created_by)

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    lookup_field = "id"

    @rate_limit(requests=5, interval=60)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @rate_limit(requests=5, interval=60)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @rate_limit(requests=5, interval=60)
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Task.objects.all()
        return Task.objects.filter(created_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            task_title = instance.title
            self.perform_destroy(instance)
            return Response(
                {"message": f'Task "{task_title}" has been deleted successfully'},
                status=status.HTTP_200_OK,
            )
        except Http404:
            return Response(
                {"message": "Task was already deleted or does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Check if user has access to the task
    if not request.user.is_staff and request.user != task.created_by:
        return Response(
            {"error": "You don't have permission to update this task"},
            status=status.HTTP_403_FORBIDDEN,
        )

    new_status = request.data.get("status")
    valid_statuses = [choice[0] for choice in Task.STATUS_CHOICES]
    if not new_status or new_status not in valid_statuses:
        return Response(
            {"error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    task.status = new_status
    task.save()
    return Response(TaskSerializer(task).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def assign_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Check if user has access to the task
    if not request.user.is_staff and request.user != task.created_by:
        return Response(
            {"error": "You don't have permission to update this task"},
            status=status.HTTP_403_FORBIDDEN,
        )

    user_id = request.data.get("user_id")
    if user_id:
        assigned_user = get_object_or_404(User, id=user_id)
        task.assigned_to = assigned_user
    else:
        task.assigned_to = None

    task.save()
    return Response(TaskSerializer(task).data)


# Admin Deletion Views
@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def admin_delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        username = user.username
        user.delete()
        return Response(
            {"message": f"User {username} has been deleted successfully"},
            status=status.HTTP_200_OK,
        )
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def admin_delete_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        task_title = task.title
        task.delete()
        return Response(
            {"message": f'Task "{task_title}" has been deleted successfully'},
            status=status.HTTP_200_OK,
        )
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def admin_bulk_delete(request):
    user_ids = request.data.get("user_ids", [])
    task_ids = request.data.get("task_ids", [])

    deleted = {"users": 0, "tasks": 0}

    if user_ids:
        deleted["users"] = User.objects.filter(id__in=user_ids).delete()[0]
    if task_ids:
        deleted["tasks"] = Task.objects.filter(id__in=task_ids).delete()[0]

    return Response(
        {"message": "Bulk deletion completed", "deleted_counts": deleted},
        status=status.HTTP_200_OK,
    )
