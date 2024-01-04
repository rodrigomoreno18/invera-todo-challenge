from datetime import datetime
import uuid
from todo_app.models import TodoTaskModel
from django.db.models import Q


class TodoTaskRepository:
    def __init__(self, user_id: int) -> None:
        self._user_id = user_id

    def retrieve_task_by_uuid(self, uuid_str: str) -> TodoTaskModel | None:
        """Retrieves a task by its UUID.
        
        Returns None if the task doesn't exist.
        """
        tasks = TodoTaskModel.objects.filter(user_id=self._user_id, uuid=uuid_str)

        return next(iter(tasks), None)

    def delete_task_by_uuid(self, uuid_str: str) -> bool:
        """Deletes a task by its UUID.
        
        Returns whether a task was deleted or not.
        """
        deleted = TodoTaskModel.objects.filter(user_id=self._user_id, uuid=uuid_str).delete()
        return deleted[0] > 0

    def mark_completed_by_uuid(self, uuid_str: str) -> bool:
        """Marks a task by completed.
        
        If the task doesn't exist, or it is already done, returns False. Otherwise, it returns True.
        """
        updated_count = TodoTaskModel.objects.filter(user_id=self._user_id, uuid=uuid_str).update(
            is_done=True
        )
        return updated_count > 0

    def create_task(self, title: str, description: str) -> TodoTaskModel:
        """Creates a task with the given title and description, and returns the model."""

        task = TodoTaskModel(user_id=self._user_id, title=title, description=description)
        task.save()
        return task

    def list_tasks(
        self, created_date: datetime | None = None, content_filter: str | None = None
    ) -> list[TodoTaskModel]:
        """Lists all tasks, optionally filtering by created date, and/or by content."""
        
        queryset = TodoTaskModel.objects.filter(user_id=self._user_id)

        if created_date is not None:
            queryset = queryset.filter(
                created_at__year=created_date.year,
                created_at__month=created_date.month,
                created_at__day=created_date.day,
            )
        
        if content_filter is not None:
            queryset = queryset.filter(
                Q(title__contains=content_filter) | Q(description__contains=content_filter)
            )
        
        return list(queryset)
