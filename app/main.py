import os
import uuid
from typing import Optional

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.Models.Task import Task, TaskDTO
from app.Models.User import User, UserDTO

app = FastAPI(title="Task Tracker", version="0.1.0")


# --- RFC7807 helpers ---
PROBLEM_CONTENT_TYPE = "application/problem+json"


def _get_correlation_id(request: Request) -> str:
    header_val = request.headers.get("X-Correlation-ID")
    try:
        if header_val:
            uuid.UUID(str(header_val))
            return str(header_val)
    except Exception:
        pass
    return str(uuid.uuid4())


def problem_response(
    request: Request,
    *,
    status: int,
    title: str,
    detail: Optional[str] = None,
    type_: str = "about:blank",
) -> JSONResponse:
    correlation_id = _get_correlation_id(request)
    body = {
        "type": type_,
        "title": title,
        "status": status,
        "detail": detail or "",
        "instance": str(request.url.path),
        "correlation_id": correlation_id,
    }
    resp = JSONResponse(status_code=status, content=body)
    resp.headers["Content-Type"] = PROBLEM_CONTENT_TYPE
    resp.headers["X-Correlation-ID"] = correlation_id
    return resp


@app.get("/health")
def health():
    return {"status": "ok"}


class ApiError(Exception):
    def __init__(self, code: str, message: str, status: int = 400):
        self.code = code
        self.message = message
        self.status = status


@app.exception_handler(ApiError)
async def api_error_handler(request: Request, exc: ApiError):
    return problem_response(
        request,
        status=exc.status,
        title=exc.code,
        detail="",
        type_="https://example.com/problems/" + exc.code,
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    detail = exc.detail if isinstance(exc.detail, str) else "HTTP error"
    return problem_response(
        request,
        status=exc.status_code,
        title="HTTP Error",
        detail=detail,
        type_="about:blank",
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return problem_response(
        request,
        status=422,
        title="Unprocessable Entity",
        detail="Request validation failed",
        type_="https://datatracker.ietf.org/doc/html/rfc4918#section-11.2",
    )


_DB = {
    "Users": [
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
        raise ApiError(code="bad_request", message="Argument exception", status=400)


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
        raise ApiError(code="bad_request", message="Argument exception", status=400)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for i in range(len(_DB["Tasks"])):
        if _DB["Tasks"][i].id == task_id:
            _DB["Tasks"].pop(i)
            return {"status": "OK"}
    raise ApiError(code="not_found", message="item not found", status=404)


# --- Secure upload endpoint ---
UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
MAX_UPLOAD_BYTES = 2 * 1024 * 1024  # 2 MiB


def _detect_mime_and_extension(data: bytes) -> Optional[tuple[str, str]]:
    # Minimal magic-byte checks for PNG, JPEG, PDF
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return ("image/png", ".png")
    if data.startswith(b"\xff\xd8\xff"):
        return ("image/jpeg", ".jpg")
    if data.startswith(b"%PDF"):
        return ("application/pdf", ".pdf")
    return None


def _ensure_upload_dir() -> None:
    if not os.path.isdir(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    _ensure_upload_dir()

    total_read = 0
    head = b""
    chunks: list[bytes] = []
    while True:
        chunk = await file.read(64 * 1024)
        if not chunk:
            break
        total_read += len(chunk)
        if total_read > MAX_UPLOAD_BYTES:
            return problem_response(
                request,
                status=413,
                title="Payload Too Large",
                detail="Upload exceeds size limit",
                type_="about:blank",
            )
        if len(head) < 8:
            head += chunk[: 8 - len(head)]
        chunks.append(chunk)

    if total_read == 0:
        return problem_response(
            request,
            status=400,
            title="bad_request",
            detail="Empty file",
            type_="https://example.com/problems/bad_request",
        )

    sig = _detect_mime_and_extension(head)
    if sig is None:
        return problem_response(
            request,
            status=415,
            title="Unsupported Media Type",
            detail="Unsupported or unrecognized file type",
            type_="about:blank",
        )

    _, ext = sig
    safe_name = f"{uuid.uuid4()}{ext}"
    dest = os.path.join(UPLOAD_DIR, safe_name)

    # Ensure canonical path remains inside UPLOAD_DIR and avoid symlinks on parent
    dest_real = os.path.realpath(dest)
    upload_dir_real = os.path.realpath(UPLOAD_DIR)
    if not dest_real.startswith(upload_dir_real + os.sep):
        return problem_response(
            request,
            status=400,
            title="bad_request",
            detail="Invalid file path",
            type_="https://example.com/problems/bad_request",
        )

    with open(dest_real, "wb") as f:
        for c in chunks:
            f.write(c)

    return {"filename": safe_name, "size": total_read}
