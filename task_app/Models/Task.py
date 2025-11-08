from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, constr
from sqlmodel import Field, SQLModel


class TaskDTO(BaseModel):
    title: constr(min_length=1, max_length=100)
    description: constr(max_length=1000)
    type: constr(max_length=50)
    status: constr(max_length=50)
    priority: int = Field(ge=0, le=5)
    tag: constr(max_length=50)
    due_at: datetime
    started_at: datetime


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(default="")
    description: str = Field(default="")
    type: str = Field(default="")
    status: str = Field(default="")
    priority: int = Field(default=0)
    tag: str = Field(default="")
    due_at: datetime = Field(default=date.min)
    started_at: datetime = Field(default=date.min)

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "type": self.type,
            "status": self.status,
            "priority": self.priority,
            "tag": self.tag,
            "due_at": self.due_at,
            "started_at": self.started_at,
        }
