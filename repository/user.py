from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from hashing import Hash
import models
import schemas


def create(request: schemas.User, db: Session):
    hashed_password = Hash.bcrypt(password=request.password)
    user = models.User(
        name=request.name,
        email=request.email,
        password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_all(db: Session):
    return db.query(models.User).all()


def get_by_id(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not models.User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found."
        )
    return user
