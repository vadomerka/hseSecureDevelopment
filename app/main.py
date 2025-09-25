from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

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


# Example minimal entity (for tests/demo)
"""
- id
- title
- description
- type
- status
- priority
- tag
- due_at
- started_at
"""
_DB = {
    "Users": [
        {"id": 1, "name": "", "email": "", "password": ""},
        {"id": 2, "name": "", "email": "", "password": ""},
    ],
    "Tasks": [
        {
            "id": 1,
            "title": "Task 1",
            "description": "",
            "type": "Task",
            "status": "",
            "priority": 0,
            "tag": "",
            "due_at": "",
            "started_at": "",
        },
        {
            "id": 2,
            "title": "Task 1",
            "description": "",
            "type": "Task",
            "status": "",
            "priority": 0,
            "tag": "",
            "due_at": "",
            "started_at": "",
        },
    ],
}


@app.get("/users")
def get_users():
    # Admin view
    return _DB["users"]


@app.get("/users/{user_id}")
def get_user(user_id: int):
    # Profile view
    for it in _DB["users"]:
        if it["id"] == user_id:
            return it
    raise ApiError(code="not_found", message="item not found", status=404)


# @app.post("/users")
# def authorize(name: str):
#     if not name or len(name) > 100:
#         raise ApiError(
#             code="validation_error", message="name must be 1..100 chars", status=422
#         )
#     item = {"id": len(_DB["items"]) + 1, "name": name}
#     _DB["items"].append(item)
#     return item
#
#
# @app.get("/items/{item_id}")
# def get_item(item_id: int):
#     for it in _DB["items"]:
#         if it["id"] == item_id:
#             return it
#     raise ApiError(code="not_found", message="item not found", status=404)
