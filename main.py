from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List
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
    course: int = Field() # описание выше
    telephone: str = Field(default = None) # описание выше + дефолтное значение будет None

"""
Ниже представлены тестовые данные
"""
user_1 = UserRegistration(username = "danil", 
                            password = "GhL6deYX", 
                            email = "danil.bakiroff84@gmail.com", 
                            telephone = "89961080357",
                            course = 5)
user_2 = UserRegistration(username = "dinis", 
                            password = "031201", 
                            email = "dinis.sachyirov84@gmail.com", 
                            telephone = "88005553535",
                            course = 5)       

"""
Список, в котором хранятся созданные ранее тестовые
объекты
"""
users = [user_1, user_2]    

"""
Ниже метод, который позволяет получить список всех пользователей
"""
@app.get("/get_users",
        tags = ["Получение пользователей"],
        summary = "Получить всех пользователей")
async def get_users():
    return users

"""
Ниже метод, который позволяет получить информацию о конкретном пользователе
"""
@app.get("/get_user",
        tags = ["Получение пользователей"],
        summary = "Получить конкретного пользователя по имени",
        response_model = UserRegistration)
async def get_users(username: str):
    for user in users:
        if user.username == username:
            return user
        raise HTTPException(status_code = 404, detail = "Такого пользователя нет")

"""
Ниже метод, который позволяет получить пользователей с искомым курсом
"""
@app.get("/get_user_course",
        tags = ["Получение пользователей"],
        summary = "Получить пользователей по курсу",
        response_model = List[UserRegistration])
async def get_users(course: int):
    answer = []
    for user in users:
        if user.course == course:
            answer.append(user)
    return answer

"""
Ниже метод, который позволяет получить пользователей по заданным параметрам
"""
@app.get("/get_user_course_username",
        tags = ["Получение пользователей"],
        summary = "Получить пользователя по параметрам",
        response_model = List[UserRegistration])
async def get_users(course: int, username: str | None = None):
    answer = [user for user in users if user.course == course]
    if username:
        answer = [user for user in answer if user.username == username]
    return answer

"""
Ниже метод, который позволяет добавить нового пользователя
"""
@app.post("/register",
            tags = ["Добавление данных"],
            summary = "Добавить пользователя")
async def register_user(user: UserRegistration):
    users.append(user)
    return {"message": "Пользователь добавлен", "user": user}

"""
Ниже метод, который позволяет обновить данные пользователя
"""
@app.put("/update",
        tags = ["Обновление данных"],
        summary = "Обновить данные",
        response_model = UserRegistration)
async def update_user(username: str, email: str | None = None, course: int | None = None):
    for user in users:
        if user.username == username:
            if email is not None:
                user.email = email
            if course is not None:
                user.course = course
            return user
    raise HTTPException(status_code=404, detail="Студента с таким именем нет")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)