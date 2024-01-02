from datetime import datetime
import uuid
from todo_app.models import TodoTaskModel
from django.db.models import Q


class TodoTaskRepository:
    def retrieve_task_by_uuid(self, uuid_str: str) -> TodoTaskModel | None:
        tasks = TodoTaskModel.objects.filter(uuid=uuid_str)

        return next(iter(tasks), None)

    def delete_task_by_uuid(self, uuid_str: str) -> bool:
        deleted = TodoTaskModel.objects.filter(uuid=uuid_str).delete()
        return deleted[0] > 0

    def mark_completed_by_uuid(self, uuid_str: str) -> bool:
        updated_count = TodoTaskModel.objects.filter(uuid=uuid_str).update(is_done=True)
        return updated_count > 0

    def create_task(self, title: str, description: str) -> TodoTaskModel:
        task = TodoTaskModel(title=title, description=description)
        task.save()
        return task

    def list_tasks(
        self, created_date: datetime | None = None, content_filter: str | None = None
    ) -> list[TodoTaskModel]:
        queryset = TodoTaskModel.objects.all()

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
