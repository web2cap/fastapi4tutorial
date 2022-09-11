import uvicorn

from fastapi import FastAPI

from . import models
from .database import engine
from .routers import blog, user


tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "blogs",
        "description": "Manage items. So _fancy_ they have their own docs.",
    },
]

app = FastAPI(openapi_tags=tags_metadata)

models.Base.metadata.create_all(bind=engine)

app.include_router(blog.router)
app.include_router(user.router)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
