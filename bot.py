# bot.py
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import MessageReactionUpdated

from config import (
    BOT_TOKEN, ADMIN_ID, MIN_MSG_LENGTH, 
    DAILY_MSG_LIMIT, DAILY_RXN_LIMIT, REACTION_REWARD, TARGET_POINTS
)
from database import db

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- 1. КОМАНДА ТЕСТ (Исправленная) ---

@dp.message(Command("test"))
async def cmd_test(message: types.Message):
    user = db.get_user(message.from_user.id)
    if user:
        # Принудительно конвертируем в нужные типы для round()
        total = float(user[2])
        d_msg = int(user[3])
        d_rxn = float(user[4])
        
        await message.reply(
            f"📊 **Твой прогресс Moji:**\n\n"
            f"🔹 Всего баллов: `{round(total, 1)}` / {TARGET_POINTS}\n"
            f"💬 Сегодня за текст: `{d_msg} / {DAILY_MSG_LIMIT}`\n"
            f"🔥 Сегодня за лайки: `{round(d_rxn, 1)} / {DAILY_RXN_LIMIT}`"
        )
    else:
        await message.reply("Напиши что-нибудь в чате, чтобы я тебя увидел!")

# --- 2. РЕАКЦИИ ---

@dp.message_reaction()
async def on_reaction(reaction: MessageReactionUpdated):
    if not reaction.user: return
    
    user_id = reaction.user.id
    username = reaction.user.username or reaction.user.full_name
    today = datetime.now().date()

    db.register_user(user_id, username)
    user = db.get_user(user_id)
    
    # Сброс лимитов (индекс даты теперь [5])
    if str(today) != str(user[5]):
        db.reset_daily_limits(user_id, today)
        user = db.get_user(user_id)

    total_pts = float(user[2])
    daily_rxn = float(user[4])

    if daily_rxn < DAILY_RXN_LIMIT and reaction.new_reaction:
        new_total = total_pts + REACTION_REWARD
        new_daily = daily_rxn + REACTION_REWARD
        db.add_rxn_point(user_id, new_total, new_daily)
        print(f"🔥 {username} +{REACTION_REWARD} за лайк. Итого: {new_total}")

# --- 3. СООБЩЕНИЯ ---

@dp.message(F.text)
async def on_message(message: types.Message):
    if message.from_user.is_bot: return

    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.full_name
    text = message.text.strip()
    today = datetime.now().date()

    db.register_user(user_id, username)
    user = db.get_user(user_id)

    # Сброс лимитов (индекс даты теперь [5])
    if str(today) != str(user[5]):
        db.reset_daily_limits(user_id, today)
        user = db.get_user(user_id)

    total_pts = float(user[2])
    daily_msg = int(user[3])

    if daily_msg < DAILY_MSG_LIMIT and len(text) >= MIN_MSG_LENGTH:
        new_total = total_pts + 1
        new_daily = daily_msg + 1
        db.add_msg_point(user_id, new_total, new_daily)
        print(f"📈 {username} +1 за текст. Итого: {new_total}")

async def main():
    db.create_tables()
    print("🚀 Moji App Bot запущен. База данных обновлена.")
    await dp.start_polling(bot, allowed_updates=["message", "message_reaction"])

if __name__ == "__main__":
    asyncio.run(main())