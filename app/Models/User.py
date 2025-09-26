from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class UserDTO(BaseModel):
    name: str
    email: str
    password: str


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default="")
    email: str = Field(default="")
    password: str = Field(default="")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
        }
