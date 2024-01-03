from datetime import datetime
import uuid
from django.test import TestCase
from todo_app.models import TodoTaskModel

from todo_app.tasks.repository import TodoTaskRepository
from utils.time import utc_datetime


class TestTodoTaskRepository(TestCase):
    def setUp(self) -> None:
        self._user_id = 42069
        self._repository = TodoTaskRepository(self._user_id)
    
    def test_create_task(self) -> None:
        title = "title"
        description = "description"

        created_task = self._repository.create_task(title, description)

        db_task = TodoTaskModel.objects.get(
            title=title, description=description, user_id=self._user_id
        )

        self.assertEqual(db_task, created_task)

        self.assertEqual(created_task.user_id, self._user_id)
        self.assertEqual(created_task.title, title)
        self.assertEqual(created_task.description, description)
        self.assertFalse(created_task.is_done)
    
    def test_delete_task(self) -> None:
        task = self._create_test_task()

        deleted = self._repository.delete_task_by_uuid(str(task.uuid))

        self.assertTrue(deleted)
        self.assertListEqual(list(TodoTaskModel.objects.all()), [])
    
    def test_delete_nonexisting_task(self) -> None:
        self._create_test_task()

        task_count = TodoTaskModel.objects.all().count()

        deleted = self._repository.delete_task_by_uuid(str(uuid.uuid4()))
        
        new_task_count = TodoTaskModel.objects.all().count()
        self.assertEqual(task_count, new_task_count)
        self.assertFalse(deleted)
    
    def test_retrieve_task(self) -> None:
        task = self._create_test_task()

        retrieved = self._repository.retrieve_task_by_uuid(str(task.uuid))

        self.assertEqual(task, retrieved)
    
    def test_retrieve_nonexistent_task(self) -> None:
        retrieved = self._repository.retrieve_task_by_uuid(str(uuid.uuid4()))

        self.assertIsNone(retrieved)
    
    def test_mark_completed(self) -> None:
        task = self._create_test_task()

        db_task = TodoTaskModel.objects.get(id=task.id)
        self.assertFalse(db_task.is_done)

        was_updated = self._repository.mark_completed_by_uuid(str(task.uuid))

        db_task.refresh_from_db()
        self.assertTrue(db_task.is_done)
        self.assertTrue(was_updated)
    
    def test_mark_completed_nonexistent_task(self) -> None:
        self._create_test_task()

        was_updated = self._repository.mark_completed_by_uuid(str(uuid.uuid4()))

        completed_task_count = TodoTaskModel.objects.filter(is_done=True).count()
        self.assertEqual(completed_task_count, 0)
        self.assertFalse(was_updated)

    def test_list_tasks_all(self) -> None:
        task1 = self._create_test_task("task1", "task description 1")
        task2 = self._create_test_task("task2", "task description 2")

        listed = self._repository.list_tasks()

        self.assertListEqual([task1, task2], listed)
    
    def test_list_tasks_filter_by_date(self) -> None:
        task1 = self._create_test_task("task1", "task description 1")
        task2 = self._create_test_task("task2", "task description 2")

        task1.created_at = utc_datetime(2023, 4, 20)
        task2.created_at = utc_datetime(2023, 6, 9)
        task1.save()
        task2.save()

        listed_one_date = self._repository.list_tasks(created_date=utc_datetime(2023, 4, 20))
        listed_empty_date = self._repository.list_tasks(created_date=utc_datetime(2024, 1, 1))

        self.assertListEqual([task1], listed_one_date)
        self.assertListEqual([], listed_empty_date)
    
    def test_list_tasks_by_content(self) -> None:
        task1 = self._create_test_task("task1", "task description 1")
        task2 = self._create_test_task("task2", "task description 2")
        
        listed_no_match = self._repository.list_tasks(content_filter="no match")
        listed_match_title = self._repository.list_tasks(content_filter="sk1")
        listed_match_description = self._repository.list_tasks(content_filter="cription 2")
        listed_match_both = self._repository.list_tasks(content_filter="task")

        self.assertListEqual([], listed_no_match)
        self.assertListEqual([task1], listed_match_title)
        self.assertListEqual([task2], listed_match_description)
        self.assertListEqual([task1, task2], listed_match_both)
    
    def test_list_tasks_by_content_and_date(self) -> None:
        task1 = self._create_test_task("task1", "task description 1")
        task2 = self._create_test_task("task2", "task description 2")

        task1.created_at = utc_datetime(2023, 4, 20)
        task2.created_at = utc_datetime(2023, 6, 9)
        task1.save()
        task2.save()

        listed_no_match = self._repository.list_tasks(
            created_date=utc_datetime(2023, 4, 20), content_filter="ksat"
        )
        listed_match_one = self._repository.list_tasks(
            created_date=utc_datetime(2023, 6, 9), content_filter="task"
        )

        self.assertListEqual([], listed_no_match)
        self.assertListEqual([task2], listed_match_one)

    def _create_test_task(
        self, title: str = "title", description: str = "description"
    ) -> TodoTaskModel:
        return TodoTaskModel.objects.create(
            user_id=self._user_id,
            title=title,
            description=description,
        )
