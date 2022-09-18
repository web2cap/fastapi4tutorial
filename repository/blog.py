from typing import Dict

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas


def get_all(db: Session):
    return db.query(models.Blog).all()


def get_by_id(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog record with id {id} is not available."
        )
    return blog


def pre_unic_field(data: Dict, db: Session):
    for key in data:
        print(f"key: {key}")
        manager = getattr(models.Blog, key)
        blogs = db.query(models.Blog).filter(manager == data[key]).first()
        if blogs:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Blog record with {key}: {data[key]} already exists.",
            )
    return True


def create(request: schemas.Blog, db: Session, current_user: models.User):
    pre_unic_field(
        {"title": request.title, "body": request.body},
        db
    )
    new_blog = models.Blog(title=request.title, body=request.body, user_id=current_user.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def pre_change_blog(blog: models.Blog, current_user: models.User):
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog record with id {id} is not available.",
        )

    if blog.first().owner.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access to editing someone else's blog is denied",
        )
    return True


def update(id: int, request: schemas.Blog, db: Session, current_user: models.User):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    pre_change_blog(blog, current_user)
    pre_unic_field(
        {"title": request.title, "body": request.body},
        db
    )
    blog.update(request.dict())
    db.commit()
    return blog.first()


def delete(id: int, db: Session, current_user: models.User):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    pre_change_blog(blog, current_user)
    blog.delete(synchronize_session=False)
    db.commit()
    return None
