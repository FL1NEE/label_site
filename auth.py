# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models import User
from database import get_db
from schemas import UserCreate, UserLogin, Token
from fastapi import Depends, HTTPException, status

SECRET_KEY: str = "your_secret_key"
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

pwd_context: CryptContext = CryptContext(
    schemes = ["bcrypt"],
    deprecated = "auto"
)
oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(
    tokenUrl = "auth/login"
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user: Optional[User] = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode: dict = data.copy()
    expire: datetime = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> dict:
    credentials_exception: HTTPException = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = \
        {
            "WWW-Authenticate": "Bearer"
        }
    )
    try:
        payload: dict = jwt.decode(
            token,
            SECRET_KEY,
            algorithms = \
            [
                ALGORITHM
            ]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user: Optional[User] = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return {"username": user.username}

def register_user(user: UserCreate, db: Session = Depends(get_db)) -> dict:
    hashed_password: str = get_password_hash(user.password)
    db_user: User = User(
        username = user.username,
        hashed_password = hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User registered successfully"}

def login_user(user: UserLogin, db: Session = Depends(get_db)) -> dict:
    db_user: Optional[User] = authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(
            status_code = 400,
            detail = "Incorrect username or password"
        )
    access_token: str = create_access_token(
        data =\
        {
            "sub": db_user.username
        }
    )
    return {"access_token": access_token, "token_type": "bearer"}
