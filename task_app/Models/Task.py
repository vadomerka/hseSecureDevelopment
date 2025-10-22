from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class TaskDTO(BaseModel):
    title: str
    description: str
    type: str
    status: str
    priority: int
    tag: str
    due_at: datetime = Field(default=date.min)
    started_at: datetime = Field(default=date.min)


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
