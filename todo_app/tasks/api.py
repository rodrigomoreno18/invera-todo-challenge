from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from todo_app.tasks.repository import TodoTaskRepository


@dataclass
class TodoTask:
    """Agnostic representation of a TO-DO task."""
    
    uuid: str
    title: str
    description: str
    created_at: datetime
    is_done: bool

    def as_dict(self) -> dict:
        return dict(
            uuid=self.uuid,
            title=self.title,
            description=self.description,
            created_at=self.created_at,
            is_done=self.is_done,
        )


class TodoTaskAPI:
    def __init__(self, task_repository: TodoTaskRepository):
        self._repository = task_repository

    def get_task(self, task_uuid: str) -> TodoTask | None:
        """Gets a task by UUID.
        
        Returns None if the task is not found.
        """
        task = self._repository.retrieve_task_by_uuid(task_uuid)

        if task is None:
            return None
        
        return TodoTask(
            uuid=task.uuid,
            title=task.title,
            description=task.description,
            created_at=task.created_at,
            is_done=task.is_done,
        )

    def create_task(self, title: str, description: str) -> TodoTask:
        """Creates a task with the given title and description.
        
        Returns the newly-created task.
        """
        task = self._repository.create_task(title, description)

        return TodoTask(
            uuid=task.uuid,
            title=task.title,
            description=task.description,
            created_at=task.created_at,
            is_done=task.is_done,
        )

    def mark_completed(self, task_uuid: str) -> bool:
        """Marks a task as completed.
        
        It returns whether a task was marked completed.
        """
        marked_completed = self._repository.mark_completed_by_uuid(task_uuid)
        return marked_completed

    def delete_task(self, task_uuid: str) -> bool:
        """Deletes a task by UUID.
        
        Returns whether a task was deleted.
        """
        return self._repository.delete_task_by_uuid(task_uuid)

    def list_tasks(
        self, created_date: datetime | None = None, content_filter: str | None = None
    ) -> list[TodoTask]:
        """Lists tasks, with optional creation date and content filters."""

        return [
            TodoTask(
                uuid=task.uuid,
                title=task.title,
                description=task.description,
                created_at=task.created_at,
                is_done=task.is_done,
            )
            for task in self._repository.list_tasks(
                created_date=created_date, content_filter=content_filter
            )
        ]

    @classmethod
    def build(cls, user_id: int) -> TodoTaskAPI:
        return TodoTaskAPI(task_repository=TodoTaskRepository(user_id))
