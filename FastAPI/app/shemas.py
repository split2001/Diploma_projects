from pydantic import BaseModel
from typing import Optional


class CreateUser(BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int


class UpdateUser(BaseModel):
    firstname: str
    lastname: str
    age: int


class CreateBook(BaseModel):
    title: str
    description: str
    author: str
    genre: str
    completed: bool


class UpdateBook(BaseModel):
    title: Optional[str]
    description: Optional[str]
    author: Optional[str]
    genre: Optional[str]
    completed: Optional[bool]


class UpdateBookStatus(BaseModel):
    completed: bool
