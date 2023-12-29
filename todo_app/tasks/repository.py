import uuid
from todo_app.models import TodoTaskModel


class TodoTaskRepository:
    def retrieve_task_by_uuid(self, uuid_str: str) -> TodoTaskModel | None:
        tasks = TodoTaskModel.objects.filter(uuid=uuid_str)

        return next(iter(tasks), None)

    def delete_task_by_uuid(self, uuid_str: str) -> bool:
        deleted = TodoTaskModel.objects.filter(uuid=uuid_str).delete()
        print(f"deleted: {deleted}")
        return deleted[0] > 0

    def mark_completed_by_uuid(self, uuid_str: str) -> bool:
        updated_count = TodoTaskModel.objects.filter(uuid=uuid_str).update(is_done=True)
        return updated_count > 0

    def create_task(self, title: str, description: str) -> TodoTaskModel:
        task = TodoTaskModel(title=title, description=description)
        task.save()
        return task

    def list_tasks(self) -> list[TodoTaskModel]:
        return TodoTaskModel.objects.all()
