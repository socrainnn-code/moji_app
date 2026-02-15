from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse # Нужно для отправки файла
from database import db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Это заставит Render открывать твой интерфейс по главной ссылке
@app.get("/")
async def serve_index():
    return FileResponse("index.html")

@app.get("/get_points/{user_id}")
async def get_points(user_id: int):
    user = db.get_user(user_id)
    if user:
        return {
            "total_points": float(user[2]),
            "username": user[1]
        }
    return {"total_points": 0, "username": "Guest"}
