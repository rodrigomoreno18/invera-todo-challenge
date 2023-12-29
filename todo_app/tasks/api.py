from dataclasses import dataclass
from datetime import datetime
from todo_app.tasks.repository import TodoTaskRepository


@dataclass
class TodoTask:
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
        task = self._repository.create_task(title, description)

        return TodoTask(
            uuid=task.uuid,
            title=task.title,
            description=task.description,
            created_at=task.created_at,
            is_done=task.is_done,
        )

    def mark_completed(self, task_uuid: str) -> bool:
        marked_completed = self._repository.mark_completed_by_uuid(task_uuid)
        return marked_completed

    def delete_task(self, task_uuid: str) -> bool:
        return self._repository.delete_task_by_uuid(task_uuid)

    def list_tasks(self) -> list[TodoTask]:
        return [
            TodoTask(
                uuid=task.uuid,
                title=task.title,
                description=task.description,
                created_at=task.created_at,
                is_done=task.is_done,
            )
            for task in self._repository.list_tasks()
        ]

    @classmethod
    def build(cls):
        return TodoTaskAPI(task_repository=TodoTaskRepository())
