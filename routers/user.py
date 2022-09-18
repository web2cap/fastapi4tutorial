from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

import database
import schemas
from repository import user


router = APIRouter(
    prefix="/user",
    tags=["Users"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.User, db: Session = Depends(database.get_db)):
    return user.create(request, db)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser])
def get_all(db: Session = Depends(database.get_db)):
    return user.get_all(db)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_by_id(id: int, db: Session = Depends(database.get_db)):
    return user.get_by_id(id, db)
