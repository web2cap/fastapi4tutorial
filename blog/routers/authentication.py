from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import database, models, schemas
from ..repository import authentication

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login", status_code=status.HTTP_200_OK)
def login(request: schemas.Login, db: Session = Depends(database.get_db)):
    return authentication.login(request, db)
