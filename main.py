import uvicorn

from fastapi import FastAPI

import models
from database import engine
from routers import authentication, blog, user


tags_metadata = [
    {
        "name": "Users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "Blogs",
        "description": "Manage items. So _fancy_ they have their own docs.",
    },
    {
        "name": "Auth",
        "description": "OAuth2 with Password (and hashing), Bearer with JWT tokens.",
    },
]

app = FastAPI(openapi_tags=tags_metadata)

models.Base.metadata.create_all(bind=engine)

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
