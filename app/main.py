from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.Models.Task import Task, TaskDTO
from app.Models.User import User, UserDTO

app = FastAPI(title="Task Tracker", version="0.1.0")


class ApiError(Exception):
    def __init__(self, code: str, message: str, status: int = 400):
        self.code = code
        self.message = message
        self.status = status


@app.exception_handler(ApiError)
async def api_error_handler(request: Request, exc: ApiError):
    return JSONResponse(
        status_code=exc.status,
        content={"error": {"code": exc.code, "message": exc.message}},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # Normalize FastAPI HTTPException into our error envelope
    detail = exc.detail if isinstance(exc.detail, str) else "http_error"
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": "http_error", "message": detail}},
    )


_DB = {
    "Users": [
        # {"id": 1, "name": "", "email": "", "password": ""},
        # {"id": 2, "name": "", "email": "", "password": ""},
        User(id=1, name="1", email="email1", password="123"),
        User(id=2, name="2", email="email1", password="123"),
    ],
    "Tasks": [
        Task(id=1, title="Task 1", type="Task"),
        Task(id=2, title="Task 2", type="Task"),
    ],
}


@app.get("/users")
def get_users():
    # Admin view
    return [x.to_json() for x in _DB["Users"]]


@app.get("/users/{user_id}")
def get_user(user_id: int):
    # Profile view
    for it in _DB["Users"]:
        if it.id == user_id:
            return it.to_json()
    raise ApiError(code="not_found", message="item not found", status=404)


@app.post("/users")
def post_user(user_dto: UserDTO):
    try:
        res = User(name=user_dto.name, email=user_dto.email, password=user_dto.password)
        _DB["Users"].append(res)
        return res.to_json()
    except Exception:
        raise ApiError(code="Bad Request", message="Argument exception", status=400)


@app.get("/tasks")
def get_tasks():
    # Admin view
    return [x.to_json() for x in _DB["Tasks"]]


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for it in _DB["Tasks"]:
        if it.id == task_id:
            return it.to_json()
    raise ApiError(code="not_found", message="item not found", status=404)


@app.post("/tasks")
def post_task(task_dto: TaskDTO):
    try:
        res = Task(
            title=task_dto.title,
            description=task_dto.description,
            type=task_dto.type,
            status=task_dto.status,
            priority=task_dto.priority,
            tag=task_dto.tag,
            due_at=task_dto.due_at,
        )
        _DB["Tasks"].append(res)
        return res.to_json()
    except Exception:
        raise ApiError(code="Bad Request", message="Argument exception", status=400)


@app.put("/tasks/{task_id}")
def put_task(task_id: int, task_dto: TaskDTO):
    task = None
    try:
        for it in _DB["Tasks"]:
            if it.id == task_id:
                task = it
    except Exception:
        raise ApiError(code="not_found", message="item not found", status=404)
    try:
        res = Task(
            id=task.id,
            title=task_dto.title,
            description=task_dto.description,
            type=task_dto.type,
            status=task_dto.status,
            priority=task_dto.priority,
            tag=task_dto.tag,
            due_at=task_dto.due_at,
        )
        for i in range(len(_DB["Tasks"])):
            if _DB["Tasks"][i].id == task_id:
                _DB["Tasks"][i] = res
        return res.to_json()
    except Exception:
        raise ApiError(code="Bad Request", message="Argument exception", status=400)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for i in range(len(_DB["Tasks"])):
        if _DB["Tasks"][i].id == task_id:
            _DB["Tasks"].pop(i)
            return {"status": "OK"}
    raise ApiError(code="not_found", message="item not found", status=404)
