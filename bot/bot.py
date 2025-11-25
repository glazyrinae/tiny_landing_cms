import os
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Путь к файлу с подписчиками (должен быть доступен в контейнере)
SUBSCRIBERS_FILE = "/app/shared/subscribers.json"

def add_subscriber(user_id: int):
    subscribers = []
    if os.path.exists(SUBSCRIBERS_FILE):
        with open(SUBSCRIBERS_FILE) as f:
            subscribers = json.load(f)
    if user_id not in subscribers:
        subscribers.append(user_id)
        with open(SUBSCRIBERS_FILE, "w") as f:
            json.dump(subscribers, f)

@dp.message(Command("start"))
async def start(message: types.Message):
    add_subscriber(message.from_user.id)
    await message.answer("✅ Вы подписаны на рассылку!")

# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())