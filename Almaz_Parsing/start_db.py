import asyncio
from db.model import *
from db.base import init_database

from parsing.initconf import config

init_database(config.database_path)

from db.base import database

async def main():
    await database.async_main()
    pass

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
        