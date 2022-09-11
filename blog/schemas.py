from pydantic import BaseModel
from typing import List


class Blog(BaseModel):
    title: str
    body: str


class BlogOrm(Blog):
    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowOnlyUser(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[BlogOrm] = []

    class Config:
        orm_mode = True


class ShowBlog(Blog):
    owner: ShowOnlyUser

    class Config:
        orm_mode = True
