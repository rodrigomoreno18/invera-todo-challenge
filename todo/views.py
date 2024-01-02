from django.contrib.auth.models import User
from rest_framework.views import Request, Response, status
from rest_framework.decorators import api_view


@api_view(["POST"])
def signup(request: Request) -> Response:
    username = request.data.get("username", None)
    email = request.data.get("email", None)
    password = request.data.get("password", None)

    if any(value is None for value in [username, email, password]):
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data=dict(message="username, email and password must be provided"),
        )

    user = User.objects.create_user(username=username, email=email, password=password)

    return Response(
        status=status.HTTP_201_CREATED,
    )