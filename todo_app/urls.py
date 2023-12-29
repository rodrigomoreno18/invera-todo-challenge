from django.urls import path

from todo_app import views


urlpatterns = [
    path("", views.TodoTasksView.as_view()),
    path("<uuid:task_uuid>/", views.TodoTaskView.as_view()),
]
