# -*- coding: utf-8 -*-
from sqlite3 import connect, Connection, Error

class DATABASE:
    """
    Класс для получения соединения с SQLite базой данных.
    Управление соединением (включая его закрытие) передается вызывающему коду.
    """

    def __init__(self, FILENAME: str) -> None:
        """
        Инициализация объекта базы данных.

        :param FILENAME: Имя файла базы данных (без расширения .db).
        """
        self.FILENAME: str = FILENAME
        self.connection: Connection | None = None

    def get_connection(self) -> Connection:
        """
        Возвращает соединение с базой данных.

        :return: Объект соединения с базой данных.
        :raises RuntimeError: Если не удалось установить соединение.
        """
        if self.connection is None:
            try:
                self.connection: Connection = connect(
                    f"{self.FILENAME}.db",
                    check_same_thread = False,
                    isolation_level = None  # Автоматически управляем транзакциями
                )
                self.connection.execute("PRAGMA foreign_keys = ON;")  # Включаем поддержку внешних ключей
            except Error as e:
                raise RuntimeError(f"Не удалось подключиться к базе данных: {e}")
        
        return self.connection
