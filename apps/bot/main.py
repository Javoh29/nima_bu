from aiogram import Bot, Dispatcher
from django.conf import settings
from apps.bot.handlers import router

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

dp.include_router(router)

async def main():
    await dp.start_polling(bot)