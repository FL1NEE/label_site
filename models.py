# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__: str = "users"

    id: Column = Column(
        Integer,
        primary_key = True,
        index = True
    )
    username: Column = Column(
        String,
        unique = True,
        index = True
    )
    hashed_password: Column = Column(String)
