from parsing.initconf import config
import asyncio

# database
from db.model import *
from db.base import init_database

init_database(config.database_path)
from db.base import database
# chat gpt
from gpt_openai.price_embeding import create_price_db

create_price_db()

# bot
from bot.start_bot import bot_main


async def main():
    await database.async_main()
    await bot_main()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
