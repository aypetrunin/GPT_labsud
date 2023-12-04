import re
from aiogram.types import Message
from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup

class BotStates(StatesGroup):
    price = State()
    choosing_price = State()
    uslugi = State()


router_chat = Router()
# Создаем экземпляр бота глобально


# from app.gpt import set_token as gpt_set_token, MODEL_TURBO, MODEL_TURBO_GPT4

# gpt_set_token(config.OPENAI_API_KEY, MODEL_TURBO)


# main.py
# from app.keyboard import router_keyboard
# from database.models import database





