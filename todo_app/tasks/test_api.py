from unittest import TestCase
from unittest.mock import Mock
import uuid
from todo_app.models import TodoTaskModel
from todo_app.tasks.api import TodoTask, TodoTaskAPI

from todo_app.tasks.repository import TodoTaskRepository
from utils.time import utc_datetime


class TestTodoTaskAPI(TestCase):
    def setUp(self) -> None:
        self._repository = Mock(spec=TodoTaskRepository)
        self._api = TodoTaskAPI(self._repository)

        self._example_uuid = uuid.uuid4()
        self._example_title = "Some title"
        self._example_description = "Some description"
        self._example_date = utc_datetime(2023, 11, 23)
    
    def test_get_task(self) -> None:
        self._repository.retrieve_task_by_uuid.return_value = self._example_task_model()

        task = self._api.get_task(self._example_uuid)

        self._repository.retrieve_task_by_uuid.assert_called_once_with(self._example_uuid)
        self.assertEqual(task, self._example_task())
    
    def test_get_nonexistent_task(self) -> None:
        self._repository.retrieve_task_by_uuid.return_value = None

        task = self._api.get_task(self._example_uuid)

        self._repository.retrieve_task_by_uuid.assert_called_once_with(self._example_uuid)
        self.assertIsNone(task)

    def test_create_task(self) -> None:
        self._repository.create_task.return_value = self._example_task_model()

        task = self._api.create_task(self._example_title, self._example_description)

        self._repository.create_task.assert_called_once_with(
            self._example_title, self._example_description
        )
        self.assertEqual(task, self._example_task())
    
    def test_mark_completed(self) -> None:
        self._repository.mark_completed_by_uuid.return_value = True

        completed = self._api.mark_completed(self._example_uuid)

        self._repository.mark_completed_by_uuid.assert_called_once_with(self._example_uuid)
        self.assertTrue(completed)

    def test_mark_completed_nonexistent_task(self) -> None:
        self._repository.mark_completed_by_uuid.return_value = False

        completed = self._api.mark_completed(self._example_uuid)

        self._repository.mark_completed_by_uuid.assert_called_once_with(self._example_uuid)
        self.assertFalse(completed)

    def test_delete_task(self) -> None:
        self._repository.delete_task_by_uuid.return_value = True

        deleted = self._api.delete_task(self._example_uuid)

        self._repository.delete_task_by_uuid.assert_called_once_with(self._example_uuid)
        self.assertTrue(deleted)
    
    def test_delete_nonexistent_task(self) -> None:
        self._repository.delete_task_by_uuid.return_value = False

        deleted = self._api.delete_task(self._example_uuid)

        self._repository.delete_task_by_uuid.assert_called_once_with(self._example_uuid)
        self.assertFalse(deleted)
    
    def test_list_tasks(self) -> None:
        self._repository.list_tasks.return_value = [self._example_task_model()]

        listed = self._api.list_tasks(created_date=self._example_date, content_filter="Some")

        self._repository.list_tasks.assert_called_once_with(
            created_date=self._example_date, content_filter="Some"
        )
        self.assertListEqual([self._example_task()], listed)

    def _example_task_model(self) -> TodoTaskModel:
        return TodoTaskModel(
            uuid=self._example_uuid,
            title=self._example_title,
            description=self._example_description,
            created_at=self._example_date,
        )

    def _example_task(self) -> TodoTask:
        return TodoTask(
            uuid=self._example_uuid,
            title=self._example_title,
            description=self._example_description,
            created_at=self._example_date,
            is_done=False,
        )