from fastapi import FastAPI
import uvicorn

from database import UsersDataBase
from models import User

from exceptions import UserAlreadyExists


app = FastAPI(
    title="Users"
)


UsersDataBase.recreate_database()


@app.get("/all_users")
def get_all_users():
    return {
        "status": 200,
        "users": UsersDataBase.all_users()
    }


@app.post("/reg")
def register(user: User):
    try:
        UsersDataBase.add_user(user)
    except UserAlreadyExists:
        return {
            "status": 400,
            "message": "Invalid id. (User already exists)."
        }

    return {
        "status": 200,
        "user": user
    }


@app.post("/user/{id}")
def get_user(id: int):
    if (user := UsersDataBase.get_user_by_id(id)) is not None:
        return {
            "status": 200,
            "user": user
        }
    
    return {
        "status": 404,
        "message": "User not found."
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)
