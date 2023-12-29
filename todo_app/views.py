from django.http import HttpRequest, HttpResponse
from django import views


class TodoTaskView(views.View):
    def get(self, request: HttpRequest) -> HttpResponse:
        task_id = request.GET["id"]

        