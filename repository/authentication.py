from datetime import timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import database
import models
import oauth2
from hashing import Hash


def login(request: OAuth2PasswordRequestForm, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user or not Hash.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Username or password wrong"
        )
    access_token_expires = timedelta(minutes=oauth2.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = oauth2.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
