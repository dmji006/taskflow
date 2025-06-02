from django.contrib import admin
from .models import User, Task, Comment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name")
    list_filter = ("is_staff", "is_active", "date_joined")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "created_by",
        "assigned_to",
        "status",
        "priority",
        "created_at",
    )
    list_filter = ("status", "priority", "created_at", "assigned_to")
    search_fields = ("title", "description", "created_by__username", "assigned_to__username")
    date_hierarchy = "created_at"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'content', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('content', 'user__username', 'task__title')
