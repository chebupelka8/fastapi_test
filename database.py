import sqlite3
from typing import Optional

from models import User

from exceptions import UserAlreadyExists


class UsersDataBase:
    __path: str = "database.db"

    @classmethod
    def create_table(cls) -> None:
        with sqlite3.connect(cls.__path) as database:
            cursor = database.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY,
                    first_name TEXT,
                    last_name TEXT
                )
                """
            )
    
    @classmethod
    def add_user(cls, user: "User") -> None:
        with sqlite3.connect(cls.__path) as database:
            cursor = database.cursor()

            if user.id not in map(lambda x: x.id, cls.all_users()):
                cursor.execute(
                    """
                    INSERT INTO users(id, first_name, last_name) VALUES(?, ?, ?)
                    """,
                    (user.id, user.first_name, user.last_name)
                )

            else:
                raise UserAlreadyExists(f"User with {user.id} id already exists.")    

    @classmethod
    def all_users(cls):
        with sqlite3.connect(cls.__path) as database:
            cursor = database.cursor()
            cursor.execute("SELECT * FROM users")

            return list(map(
                lambda user: User(id=user[0], first_name=user[1], last_name=user[2]), 
                cursor.fetchall()
            ))
    
    @classmethod
    def get_user_by_id(cls, id: int) -> Optional[User]:
        for user in cls.all_users():
            if user.id == id:
                return user
        
        return None
    
    @classmethod
    def recreate_database(cls) -> None:
        with sqlite3.connect(cls.__path) as database:
            cursor = database.cursor()
            cursor.execute(
                """
                DROP TABLE users
                """
            )
        
        cls.create_table()



