from aiogram import types
from db.base import async_session
from db.models import User, UserMessage,  ErrorLog, Rating, now, TgUser, ApiUser
from sqlalchemy import select, update, engine
from sqlalchemy.sql import Executable
from sqlalchemy.orm import aliased
from gptindex.gptutils import num_tokens_from_string
from typing import Optional
from utils.logger import logger
from ixconfig import ixconfig
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
class RequestsDBData:
    def __init__(self):
        self.quota = ixconfig.maxquota
        self.dt_startquota = now()
        self.dialog = 1
        self.api_key = None
        self.messages = []
    def clear(self):
        self.messages.clear()
        self.quota = ixconfig.maxquota
        self.dt_startquota = now()


class RequestsDB:
    def __init__(self, d:RequestsDBData = None):
        self.dt = now()
        self.message_id = 0
        self.telegram_id = 0
        self.chat_id = 0
        self.user_id = 0
        self.user_tg_id = 0
        self.user_api_id = ""
        self.user_first_name = ""
        self.user_last_name = ""
        self.username = 0
        self.usermessage_id = 0
        self.session:AsyncSession = async_session()
        self.data = d
        self.data = RequestsDBData()
    def set_message(self,  m: types.Message):
        if m:
            self.message_id = m.message_id
            self.telegram_id = m.message_id
            self.chat_id = m.chat.id
            self.user_id = 0
            self.user_tg_id = m.from_user.id
            self.username = m.from_user.username
            fu = m.from_user
            self.user_first_name = fu.first_name
            self.user_last_name = fu.last_name

            self.usermessage_id = 0

    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None

    def open(self):
        self.session = async_session()

    async def execute(self, stmt:Executable):
        """ stmt = update(User).where(User.tg_id == tg_user_id).values(dialog_state=dialog_state, dialog_score=dialog_score)
            select(UserMessage).where(UserMessage.id == self.user_message_id)
        """

        result = await self.session.execute(stmt)
        await self.session.commit()
        return result
    async def add(self, obj:object):
        self.session.add(obj)
        await self.session.commit()

    async def get(self, stmt:Executable)->engine.Result[Any]:
        result = await self.session.execute(stmt)
        return result

    async def update_user(self):
        dt = now()
        tu = TgUser
        u = User
        q: engine.Result = await self.get(
            select(tu.id, u.quota, u.dt_startquota, u.dialog).select_from(tu).join(u, u.id == tu.id).where(tu.tg_id == self.user_tg_id)
        )
        u = self
        data = u.data
        r = q.first()
        if r:
            u.user_id, data.quota, data.dt_startquota, data.dialog = r
        else:
            user = User(
                refid = f"tg:{u.user_tg_id}",
                username=u.username,
                first_name =  u.user_first_name,
                last_name = u.user_last_name,
                # e_mail = fu.url,
                quota = data.quota,
                dt_startquota =dt,
                dialog = data.dialog,
            )
            await self.add(user)
            self.user_id = user.id
            tg = TgUser(
                tg_id=u.user_tg_id,
                id = self.user_id
            )
            await self.add(tg)
        if data.dt_startquota==None or (dt-data.dt_startquota).seconds > 10*3600:
            data.quota = ixconfig.maxquota
            data.dt_startquota = dt
        print(self.user_id)

    async def update_apiuser(self):
        dt = now()
        au = ApiUser
        u = User
        q: engine.Result = await self.get(
            select(au.id, u.quota, u.dt_startquota, u.dialog).select_from(au).join(u, u.id == au.id).where( au.api_id == self.user_api_id)
        )
        u = self
        data = u.data
        r = q.first()
        if r:
            u.user_id, data.quota, data.dt_startquota, data.dialog = r
        else:
            user = User(
                refid = f"api:{u.user_api_id}",
                username=u.username,
                first_name =  u.user_first_name,
                last_name = u.user_last_name,
                # e_mail = fu.url,
                quota = data.quota,
                dt_startquota =dt,
                dialog = data.dialog,
            )
            await self.add(user)
            self.user_id = user.id
            tg = ApiUser(
                api_id=u.user_api_id,
                id = self.user_id
            )
            await self.add(tg)
        if data.dt_startquota==None or (dt-data.dt_startquota).seconds > 10*3600:
            data.quota = ixconfig.maxquota
            data.dt_startquota = dt
        print(self.user_id)


    async def update_data(self):
        u = aliased(User,name="u")
        data = self.data
        await self.execute(stmt= update(u).where(u.id == self.user_id).values(
            quota = data.quota,
            dt_startquota = data.dt_startquota,
            dialog = data.dialog
        ))

    async def new_usermessage(self, message_text):
        u = self
        message = UserMessage(
            chat_id= u.chat_id,
            user_id= u.user_id,
            u_message= message_text,
            u_message_id = u.message_id,
            u_tokens =  num_tokens_from_string(message_text)
        )
        await self.add(message)
        self.usermessage_id =  message.id
        print(f"self.usermessage_id = {self.usermessage_id}")

    async def get_usermessage(self):
        if self.usermessage_id == 0:
            return
        r = await self.get(select(UserMessage).where(UserMessage.id == self.usermessage_id))
        return r.first()

    async def answer_usermessage(self, message_id, answer, prompt_tokens=0, completion_tokens=0):
        self.data.quota -= prompt_tokens + completion_tokens*2
        m = UserMessage
        dt2 = now()
        sec = (dt2 - self.dt).total_seconds()
        print(f"self.usermessage_id = {self.usermessage_id}")
        await self.execute(
            stmt = update(m).where(m.id == self.usermessage_id).values(
                a_message = answer,
                a_message_id = message_id,
                a_tokens = num_tokens_from_string(answer),
                prompt_tokens = prompt_tokens,
                completion_tokens = completion_tokens,
                dt_answer = dt2,
                time_duration = sec
            )
        )

    async def add_rating(self,  rate):
        m = UserMessage
        await self.execute(
            stmt=update(m).where(m.id == self.usermessage_id).values(
                rating=rate,
                dt_rating = now()
            )
        )
        u = self
        rating = Rating(
            chat_id = u.chat_id,
            user_id=u.user_id,
            message_id = u.message_id,
            user_message_id = u.usermessage_id,
            rating = rate
        )
        await self.add(rating)

    async def add_log(self, func: str, param: str, text: str):
        u = self
        log = ErrorLog(
            chat_id=u.chat_id,
            user_id=u.user_id,
            user_message_id=u.usermessage_id,
            function_name = func,
            arguments = param,
            error_message = text
        )
        await self.add(log)
