from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt

from app.models import User
from .config import settings
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime
from .schemas  import TokenData
from .database import get_db
from sqlalchemy import or_


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict, expire_time: timedelta = None):
    to_encode = data.copy()
    if expire_time:
        expire = datetime.utcnow()+expire_time
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('nick_name')

        if id is None:
            raise credentials_exception

        token_data = TokenData(id=id)

    except Exception:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")
    token = verify_access_token(token, credentials_exception)

    user = db.query(User).filter(User.nick_name == token.id).first()

    return user


def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")
    token = verify_access_token(token, credentials_exception)

    user = db.query(User).filter(
        User.nick_name == token.id,
        or_(
            User.role == "admin",
            User.role == "superuser"
        )
    ).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to perform the requested action")

    return user


def get_current_agent(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")
    token = verify_access_token(token, credentials_exception)

    user = db.query(User).filter(
        User.nick_name == token.id,
        or_(
            User.role == "agent",
            User.role == "superuser"
        )
    ).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to perform the requested action")

    return user


