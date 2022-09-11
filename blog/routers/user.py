from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import database, models, schemas
from ..hashing import Hash


router = APIRouter()


@router.post("/user", status_code=status.HTTP_201_CREATED, tags=["users"])
def create(request: schemas.User, db: Session = Depends(database.get_db)):
    hashed_password = Hash.bcrypt(password=request.password)
    blog = models.User(
        name=request.name,
        email=request.email,
        password=hashed_password
    )
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog


@router.get("/user", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser], tags=["users"])
def get_all(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users


@router.get("/user.{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser, tags=["users"])
def get_by_id(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found."
        )
    return user
