# -*- coding: utf-8 -*-
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models import Base
from database import get_db
from auth import get_current_user, register_user, login_user
from schemas import UserCreate, UserLogin, Token

app: FastAPI = FastAPI()

# Создаем таблицы в базе данных
Base.metadata.create_all(
	bind = get_db().bind
)

@app.get("/")
def home():
    return {"message": "Добро пожаловать на главную страницу!"}

@app.get("/artists/")
def artists():
    return {"message": "Это раздел артистов."}

@app.post("/auth/register/")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(user, db)

@app.post("/auth/login/", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(user, db)

@app.get("/auth/")
def auth_panel(current_user: dict = Depends(get_current_user)):
    return {"message": f"Добро пожаловать в личный кабинет, {current_user['username']}!"}
