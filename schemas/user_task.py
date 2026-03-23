from pydantic import BaseModel, Field
from typing import Annotated, Literal


class UserCreate(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=50)]
    email: Annotated[str, Field(min_length=5, max_length=100)]
    password: Annotated[str, Field(min_length=6, max_length=100)]
    role: Literal["admin", "user"] = "user"


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
