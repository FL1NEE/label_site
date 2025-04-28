# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_handler import DATABASE

# Используем DB_HANDLER для подключения к базе данных
db_handler: DATABASE = DATABASE("label_site")

def get_db():
    """
    Генератор для получения сессии базы данных.
    """
    connection: Connection = db_handler.get_connection()
    try:
        yield connection
    finally:
        connection.close()
