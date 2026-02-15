# api.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import db  # Импортируем твой готовый менеджер базы

app = FastAPI()

# Настройка CORS (чтобы браузер разрешил фронтенду забирать данные)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Разрешаем запросы ототовсюду (для разработки)
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get_points/{user_id}")
async def get_points(user_id: int):
    """Эндпоинт, который отдает баллы конкретного юзера"""
    user = db.get_user(user_id)
    if user:
        # Индексы из нашей таблицы (всего 6 колонок):
        # 0: id, 1: username, 2: total, 3: d_msg, 4: d_rxn, 5: date
        return {
            "user_id": user[0],
            "username": user[1],
            "total_points": float(user[2]),
            "daily_msg": int(user[3]),
            "daily_rxn": float(user[4])
        }
    else:
        # Если юзера нет, возвращаем нули (чтобы фронтенд не падал)
        return {
            "user_id": user_id, 
            "total_points": 0, 
            "daily_msg": 0, 
            "daily_rxn": 0
        }

@app.get("/")
async def root():
    return {"status": "Moji API is working!"}