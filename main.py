from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, ConfigDict
import uvicorn


app = FastAPI()

class STaskAdd(BaseModel):
    name: str # определяет поле, которое должен содержать объект (тип "строка")
    description: str | None = None # описание выше + дефолтное значение будет None

class STask(STaskAdd):
    id: int # определяет поле, которое должен содержать объект (тип "int")
    model_config = ConfigDict(from_attributes = True) # позволяеь создавать объект модели напрямую из атрибутов Python-объектов

@app.post("/",
            tags = ["Добавление данных"],
            summary = "Добавить данные")
async def add_task(task: STaskAdd = Depends()):
    return {"data": task}

@app.get("/",
        tags = ["Получение данных"], # задать тэг (титул для распределения запросов (по сути просто для красоты))
        summary = "Получить ответ" # псевдоним функциям, которые определены после декоратора
        )
async def home():
    return {"data": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)