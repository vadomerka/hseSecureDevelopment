from typing import Optional

from pydantic import BaseModel, EmailStr, constr
from sqlmodel import Field, SQLModel


class UserDTO(BaseModel):
    name: constr(min_length=1, max_length=100)
    email: EmailStr
    password: constr(min_length=8, max_length=128)


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
        }
