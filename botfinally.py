import logging
import os
from telegram import Update, ForceReply
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv
import nest_asyncio
import asyncio

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Применяем nest_asyncio
nest_asyncio.apply()

# Загружаем переменные окружения из .env файла
dotenv_path = 'key.env'  
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    logger.info(f'Загружен файл окружения из {dotenv_path}')
else:
    logger.error(f'Файл окружения {dotenv_path} не найден')

# Выводим все переменные окружения для отладки
logger.info("Все переменные окружения:")
for key, value in os.environ.items():
    logger.info(f'{key}: {value}')

# Получаем токен из переменных окружения
token = os.getenv("TELEGRAM_TOKEN")
logger.info(f"Значение token: {token}")
if not token:
    logger.error("TELEGRAM_TOKEN не найден в переменных окружения")
    exit(1)

# Определяем обработчики команд
async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf'Привет, {user.mention_html()}! Я ваш бот.',
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Помощь!')

async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(update.message.text)

def initialize_application(token: str):
    logger.info("Запуск бота...")
    return ApplicationBuilder().token(token).build()


async def main() -> None:
    # Создаем объект Application
    application = initialize_application(token)

    if application is None or application.bot is None:
        logger.error("Не удалось создать объект Application.")
        return

    logger.info("Объект Application успешно создан.")

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Регистрируем обработчик для текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запускаем бота и ожидаем сообщений
    logger.info("Бот запущен. Ожидание сообщений...")
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
