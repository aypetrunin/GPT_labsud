from parsing.conf import config
from aiogram import Bot, Dispatcher
from bot.bot import router_chat
from bot.different_types import router as router_diff
import bot.commands 
import bot.price

async def bot_main():
    dp = Dispatcher()
    bot = Bot(token=config.TG_TOKEN)

    dp.include_routers(router_chat, router_diff)
#    dp.include_router(router_keyboard)
    print('Бот успешно запущен!')
    await dp.start_polling(bot)
