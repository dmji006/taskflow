from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Task, Comment


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "password2",
            "email",
            "first_name",
            "last_name",
            "photo",
        )
        extra_kwargs = {
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "photo": {"required": False},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "photo",
            "is_active",
            "date_joined",
            "last_login",
        ]
        read_only_fields = ["id", "date_joined", "last_login"]


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Comment
        fields = ('id', 'task', 'user', 'content', 'created_at', 'updated_at')
        read_only_fields = ('id', 'task', 'created_at', 'updated_at')


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.CharField(source='assigned_to.username', read_only=True)
    created_by = serializers.IntegerField(source="created_by.id", read_only=True)
    assigned_to_id = serializers.IntegerField(
        write_only=True, required=False, allow_null=True
    )
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "assigned_to",
            "assigned_to_id",
            "created_by",
            "status",
            "priority",
            "created_at",
            "updated_at",
            "comments"
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def create(self, validated_data):
        assigned_to_id = validated_data.pop("assigned_to_id", None)
        if assigned_to_id:
            validated_data["assigned_to"] = User.objects.get(id=assigned_to_id)
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        assigned_to_id = validated_data.pop("assigned_to_id", None)
        if assigned_to_id:
            instance.assigned_to = User.objects.get(id=assigned_to_id)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
