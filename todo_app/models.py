import uuid
from django.db import models


class TodoTaskModel(models.Model):
    id = models.BigAutoField(primary_key=True)

    # Used to hide internal id in requests
    uuid = models.UUIDField(default=uuid.uuid4)

    title = models.CharField(max_length=256, null=False)
    description = models.TextField()
    is_done = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "todo_task"

        unique_together = [
            ["uuid"],
        ]
        indexes = [
            models.Index(fields=["is_done"], name="is_done_idx"),
        ]