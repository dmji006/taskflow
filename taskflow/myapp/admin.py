from django.contrib import admin
from .models import User, Task


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
        "status",
        "priority",
        "created_at",
    )
    list_filter = ("status", "priority", "created_at")
    search_fields = ("title", "description")
    date_hierarchy = "created_at"
