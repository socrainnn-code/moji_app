# api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse # Импортируем это!
from database import db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ИСПРАВЛЕННЫЙ БЛОК: Теперь по главной ссылке откроется сайт
@app.get("/")
async def serve_index():
    return FileResponse("index.html") 

@app.get("/get_points/{user_id}")
async def get_points(user_id: int):
    user = db.get_user(user_id)
    if user:
        return {
            "user_id": user[0],
            "username": user[1],
            "total_points": float(user[2]),
            "daily_msg": int(user[3]),
            "daily_rxn": float(user[4])
        }
    return {"total_points": 0, "username": "Guest"}
