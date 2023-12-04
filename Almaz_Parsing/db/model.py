from db.base import Base, moscow_tz
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Time, Boolean, DATETIME
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)  # ID от Telegram
    username = Column(String(100))
    date = Column(Date, default=lambda: datetime.now(moscow_tz).date())
    time = Column(Time, default=lambda: datetime.now(moscow_tz).time())
    dt_create = Column(DATETIME, default=lambda: datetime.now(moscow_tz))

class ErrorLog(Base):  # фиксация ошибок
    __tablename__ = 'error_logs'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    function_name = Column(String(255))  # имя функции, которая вызвала ошибку
    arguments = Column(String(255))  # аргументы, переданные в функцию
    error_message = Column(String(255))  # сообщение об ошибке

class Rating(Base):    # оценка ответов
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, default=lambda: datetime.now(moscow_tz).date())
    time = Column(Time, default=lambda: datetime.now(moscow_tz).time())
    q_message_id = Column(Integer)  # ID сообщения в телеграмм
    q_chat_id = Column(Integer)
    q_user_id = Column(Integer)  # ID пользователя в телеграмм
    q_message = Column(String(3000))
    a_message_id = Column(Integer)  # ID сообщения в телеграмм
    a_message = Column(String(3000))
    a_rating = Column(Integer)
    rating_datetime = Column(Date, default=lambda: datetime.now(moscow_tz))
    q_tokens = Column(Integer)
    a_tokens = Column(Integer)
    total_tokens = Column(Integer)
