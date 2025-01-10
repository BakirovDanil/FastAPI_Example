from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import uvicorn

"""
Создание объекта класса
"""
app = FastAPI()

"""
Создание класса, который определяет модель (структуру)
добавляемых данных (объектов) с определенными полями
"""
class UserRegistration(BaseModel):
    username: str = Field() # определяет поле, которое должен содержать объект (тип "строка")
    password: str = Field() # описание выше + дефолтное значение будет None
    email: str = Field() # описание выше
    telephone: str = Field(default = None) # описание выше + дефолтное значение будет None

"""
Ниже представлены тестовые данные
"""
user_1 = UserRegistration(username = "danil", 
                            password = "GhL6deYX", 
                            email = "danil.bakiroff84@gmail.com", 
                            telephone = "89961080357")
user_2 = UserRegistration(username = "dinis", 
                            password = "031201", 
                            email = "dinis.sachyirov84@gmail.com", 
                            telephone = "88005553535")       

users = [user_1, user_2]    

@app.get("/get_users",
        tags = ["Получение пользователей"],
        summary = "Получить всех пользователей")
async def get_users():
    return users

@app.get("/get_user",
        tags = ["Получение пользователей"],
        summary = "Получить конкретного пользователя",
        response_model = UserRegistration)
async def get_users(username: str):
    for user in users:
        if user.username == username:
            return user
        raise HTTPException(status_code = 404, detail = "Такого пользователя нет")

@app.post("/register",
            tags = ["Добавление данных"],
            summary = "Добавить данные",
            response_model = UserRegistration)
async def register_user(user: UserRegistration):
    users.append(user)
    return {"message": "Пользователь добавлен", "user": user}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)