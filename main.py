# main.py
import asyncio
import uvicorn
from api import app as fastapi_app
from bot import dp, bot, db
import logging

# Настраиваем логи, чтобы видеть, что происходит в облаке
logging.basicConfig(level=logging.INFO)

async def run_bot():
    db.create_tables()
    logging.info("🚀 Бот запущен!")
    await dp.start_polling(bot, allowed_updates=["message", "message_reaction"])

async def run_api():
    config = uvicorn.Config(fastapi_app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    logging.info("🔌 API запущено на порту 8000")
    await server.serve()

async def main():
    # Запускаем бота и API одновременно
    await asyncio.gather(
        run_bot(),
        run_api()
    )

if __name__ == "__main__":
    asyncio.run(main())