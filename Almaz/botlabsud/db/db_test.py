from db.base import async_session, init_database
from db.models import  User, now
from  utils.logger import logger
from sqlalchemy import select, engine
from db.botdb import BotDB, types


class Test:
    def __init__(self):
        self.db= BotDB()
        db = self.db
        db.user_tg_id = 409521+4
        db.username = "Test"
        db.user_id = 0

    @logger.catch
    async def test1(self):
        print("dfasdf")
        await self.db.update_user()


    @logger.catch
    async def test2(self):
        session =  async_session()
        result = await session.execute(
            select(User.id).where(User.tg_id == self.user_tg_id)
        )
        self.user_id = result.scalar_one_or_none()
        u = self
        if not self.user_id:
            user = User(
                tg_id=u.user_tg_id,
                username=u.username,
            )
            session.add(user)
            await session.commit()
            self.user_id = user.id
        await session.close()

    async def test3(self):
        b = BotDB(None)
        b.user_id = self.user_id
        # await b.update_user()
        await b.new_usermessage("Test")
        await b.answer_usermessage(0, "Answer")
        await b.add_rating(2)
        await b.add_log("-","p","Error")
