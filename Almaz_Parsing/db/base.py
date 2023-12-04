import pytz
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


#from config import SQLALCHEMY

moscow_tz = pytz.timezone('Europe/Moscow') # Определение часового пояса
database = None
async_session = None

class db_class:
    def __init__(self, database_path) -> None:
        self.engine = create_async_engine(database_path, echo=True)
        self.async_session = async_sessionmaker(self.engine)
        pass
    async def async_main(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

# Выносим все зависимости от настроек

def init_database(database_path):
    global database
    global async_session
    database = db_class(database_path)
    async_session = database.async_session

class Base(AsyncAttrs, DeclarativeBase):
    pass
