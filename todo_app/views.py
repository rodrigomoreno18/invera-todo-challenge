from rest_framework.views import APIView, Request, Response, status
from rest_framework.permissions import IsAuthenticated

from todo_app.serializers import TodoTaskSerializer
from todo_app.tasks.api import TodoTaskAPI
from utils.time import parse_datetime


class TodoTasksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        task_api = TodoTaskAPI.build(request.user.id)

        created_at_filter = request.query_params.get("created_at")
        content_filter = request.query_params.get("includes")

        if created_at_filter is not None:
            created_at_filter = parse_datetime(created_at_filter)
        
        tasks = task_api.list_tasks(created_date=created_at_filter, content_filter=content_filter)
        return Response(
            status=status.HTTP_200_OK, data=[task.as_dict() for task in tasks]
        )

    def post(self, request: Request) -> Response:
        serializer = TodoTaskSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        task_data = serializer.validated_data

        task_api = TodoTaskAPI.build(request.user.id)
        task = task_api.create_task(task_data["title"], task_data["description"])

        return Response(
            status=status.HTTP_201_CREATED,
            data=task.as_dict(),
        )


class TodoTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, task_uuid: str) -> Response:
        task_api = TodoTaskAPI.build(request.user.id)

        task = task_api.get_task(task_uuid)
        if task is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
        return Response(
            dict(uuid=task.uuid, title=task.title, description=task.description, is_done=task.is_done)
        )

    def patch(self, request: Request, task_uuid: str) -> Response:
        task_api = TodoTaskAPI.build(request.user.id)

        if request.query_params.get("is_done", False):
            marked_completed = task_api.mark_completed(task_uuid)
            return Response(status=status.HTTP_200_OK, data=dict(updated=marked_completed))

        return Response(status=status.HTTP_200_OK, data=dict(updated=False))


    def delete(self, request: Request, task_uuid: str) -> Response:
        task_api = TodoTaskAPI.build(request.user.id)

        was_deleted = task_api.delete_task(task_uuid)
        if was_deleted:
            return Response(status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_404_NOT_FOUND, data=dict(id=task_uuid))
