from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn


app = FastAPI()

books = [
    {
        "id": 1,
        "name": "Python для новичков",
        "Author": "ДДТ"
    },
    {
        "id": 2,
        "name": "Python для продвинутых",
        "Author": "БДТ"
    },
]

@app.get("/books",
        tags = ["Книга"], # задать тэг (титул для распределения запросов (по сути просто для красоты))
        summary = "Получить все книги"
        )
def read_books():
    return books

@app.get("/books/{book_id}",
        tags = ["Книга"],
        summary = "Получить конкретную книгу")
def get_books(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code = 404, detail = "Данная книга не найдена. Проверьте входящие данные")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)