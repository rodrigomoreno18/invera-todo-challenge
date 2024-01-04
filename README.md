# Invera TODO Challenge

Este proyecto implementa una simple API que permite crear y administrar tareas (TO-DO).

Las principales funcionalidades ofrecidas son:

- Crear una cuenta con usuario y contraseña
- Iniciar sesión
- Crear tareas con título y descripción
- Listar tareas, opcionalmente filtrando por día y/o por contenido de las mismas
- Eliminar tareas
- Marcar tareas como completas

## Inicio rápido

```bash
# Clonar el repositorio
. $ git clone git@github.com:rodrigomoreno18/invera-todo-challenge.git

# Entrar al directorio
. $ cd invera-todo-challenge

# Armar la imagen
invera-todo-challenge $ docker build . -t invera-todo

# Iniciar la app
invera-todo-challenge $ docker run --rm -it -p 8000:8000 --name invera_todo -d invera-todo

# Aplicar migraciones
invera-todo-challenge $ docker exec -it invera_todo python manage.py migrate
```

### API

> (Ejemplos usando cURL)

```bash
# signup: POST /signup/
curl http://localhost:8000/signup/ \
-d username=<your_user_name> \
-d password=<your_password> \
-d email=<your_email> # (optional)
```

```bash
# login: POST /login/
curl http://localhost:8000/login/ \
-d username=<your_user_name> \
-d password=<your_password>

Response:
{
    "token": string
}
```

```bash
# list tasks: GET /todo/
curl http://localhost:8000/todo/ \
-H "Authorization: Token <auth-token>" \
--url-query "created_at=<YYYY-MM-DD>" \ # (optional)
--url-query "includes=<some_text>" # (optional)

Response:
[
    {
        "uuid": string,
        "title": string,
        "description": string,
        "created_at": string date,
        "is_done": boolean
    },
    ...
]
```

```bash
# get task: GET /todo/:uuid/
curl http://localhost:8000/todo/:uuid/ \
-H "Authorization: Token <auth-token>"

Response:
{
    "uuid": string,
    "title": string,
    "description": string,
    "created_at": string date,
    "is_done": boolean
}
```

```bash
# delete task: DELETE /todo/:uuid/
curl -X DELETE http://localhost:8000/todo/:uuid/ \
-H "Authorization: Token <auth-token>"
```

```bash
# mark task as completed: PATCH /todo/:uuid/
curl -X PATCH http://localhost:8000/todo/:uuid/ \
-H "Authorization: Token <auth-token>" \
--url-query is_done=true

Response:
{
    "updated": boolean
}
```
