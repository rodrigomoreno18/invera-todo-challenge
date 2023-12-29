import uuid
from todo_app.models import TodoTask


class TodoTaskRepository:
    def retrieve_task_by_uuid(self, uuid_str: str) -> TodoTask | None:
        if not self._is_uuid_valid(uuid_str):
            return None
        
        tasks = TodoTask.objects.filter(uuid=uuid_str)

        return next(iter(tasks), None)

    def create_task(self, title: str, description: str) -> TodoTask:
        task = TodoTask(title=title, description=description)
        task.save()
        return task
    
    def _is_uuid_valid(self, uuid_str: str) -> bool:
        try:
            uuid_object = uuid.UUID(uuid_str)
        except ValueError:
            return False
        else:
            return True