from rest_framework import serializers

from todo_app.models import TodoTaskModel


class TodoTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoTaskModel
        fields = ["uuid", "title", "description", "created_at", "is_done"]