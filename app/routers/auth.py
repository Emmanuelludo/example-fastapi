from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import UserLogin, Token
from .. import models
from .. import utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])


@router.post('/login',)
# original using UserLogin .email schema
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not (user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")
    access_token = oauth2.create_acces_token(
        data={"user_id": user.id})

    return {'token': access_token, 'token_type': 'bearer'}
