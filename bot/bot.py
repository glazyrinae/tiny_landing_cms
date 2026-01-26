import os
import json
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

SUBSCRIBERS_FILE = "/app/shared/subscribers.json"

def add_subscriber(user_id: int):
    """Добавление подписчика в файл"""
    subscribers = []
    if os.path.exists(SUBSCRIBERS_FILE):
        with open(SUBSCRIBERS_FILE, "r") as f:
            subscribers = json.load(f)
    if user_id not in subscribers:
        subscribers.append(user_id)
        with open(SUBSCRIBERS_FILE, "w") as f:
            json.dump(subscribers, f)
        logger.info(f"Добавлен подписчик: {user_id}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user_id = update.effective_user.id
    add_subscriber(user_id)
    await update.message.reply_text("✅ Вы подписаны на рассылку!")

def main():
    """Запуск бота"""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN не найден в переменных окружения")
        return

    try:
        # Создаем Application с настройками таймаутов
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Добавляем обработчики
        application.add_handler(CommandHandler("start", start))
        
        logger.info("Бот запускается...")
        
        # Запускаем polling с настройками
        application.run_polling(
            poll_interval=1.0,  # Интервал между запросами
            timeout=30,         # Таймаут запроса
            drop_pending_updates=True  # Игнорировать старые updates при старте
        )
        
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")

if __name__ == "__main__":
    main()