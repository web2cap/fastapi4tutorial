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


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[BlogOrm] = []

    class Config:
        orm_mode = True


class ShowBlog(Blog):
    owner: ShowUser

    class Config:
        orm_mode = True
