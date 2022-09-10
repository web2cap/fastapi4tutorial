import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status  # Response
from sqlalchemy.orm import Session
from typing import List


from . import models, schemas
from .database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close_all()


@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog", response_model=List[schemas.ShowBlog])
def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_by_id(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog record with id {id} is not available."
        )
    return blog


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog record with id {id} is not available."
        )
    blog.delete(synchronize_session=False)
    db.commit()
    return None


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_by_id(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog record with id {id} is not available.",
       )
    blog.update(request.dict())
    db.commit()
    return blog.first()


# USERS

@app.post("/user", status_code=status.HTTP_201_CREATED)
def create(request: schemas.User, db: Session = Depends(get_db)):
    blog = models.User(
        name=request.name,
        email=request.email,
        password=request.password
    )
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog


@app.get("/user", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser])
def get_all(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.get("/user.{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found."
        )
    return user


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
