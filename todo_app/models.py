import uuid
from django.db import models


class TodoTaskModel(models.Model):
    id = models.BigAutoField(primary_key=True)

    # Used to hide internal id in requests
    uuid = models.UUIDField(default=uuid.uuid4)

    user_id = models.PositiveIntegerField(null=False)

    title = models.CharField(max_length=256, null=False)
    description = models.TextField()
    is_done = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "todo_task"

        unique_together = [
            ["user_id", "uuid"],
        ]
        indexes = [
            models.Index(fields=["user_id", "is_done"], name="is_done_idx"),
            models.Index(fields=["user_id", "created_at"], name="created_at_idx"),
            # TODO: check if title/description should use an index (given we can filter by content)
        ]