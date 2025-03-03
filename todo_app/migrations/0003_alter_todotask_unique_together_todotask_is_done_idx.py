# Generated by Django 5.0 on 2023-12-29 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("todo_app", "0002_todotask_is_done_todotask_uuid"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="todotask",
            unique_together={("uuid",)},
        ),
        migrations.AddIndex(
            model_name="todotask",
            index=models.Index(fields=["is_done"], name="is_done_idx"),
        ),
    ]
