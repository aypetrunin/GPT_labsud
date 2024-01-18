from bot.bot import router_chat as router, BotStates
from aiogram import filters, types, F
from aiogram.fsm.context import FSMContext
from bot.bot_constants import bot_constants
from bot.gpt_bot import gpt_helper
from db.botdb import BotDB


@router.message(filters.Command("start"))
async def cmd_start(message: types.Message, state:FSMContext):
    await message.answer( bot_constants.start, reply_markup=types.ReplyKeyboardRemove())
    h = gpt_helper(message, state)
    await h.select_choice(BotStates.chatgpt, bot_constants.char_gpt)

@router.message(filters.Command("api_key"))
@router.message(filters.Command("api"))
async def cmd_api(message: types.Message, state:FSMContext):
    h = gpt_helper(message, state)
    await h.select_choice(BotStates.api_key, bot_constants.api_key)

@router.callback_query(lambda c: c.data.startswith('rate_'))
async def handle_rating(callback_query: types.CallbackQuery):
    print("rate", callback_query.data)
    data_parts = callback_query.data.split('_') # Разделяем данные в callback_data
    uid, rate = map(int,data_parts[1:])
    await callback_query.message.answer(text =f"оценка {rate}",reply_markup= types.ReplyKeyboardRemove())
    text = callback_query.message.text
    print(text)
    await callback_query.message.edit_text(text = text, reply_markup=None)
    db = BotDB(callback_query.message)
    db.usermessage_id = uid
    await db.add_rating(rate)

@router.message(filters.Command(commands=["clear"]))
@router.message(filters.Command(commands=["cancel"]))
@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: types.Message, state:FSMContext):
    h = gpt_helper(message, state)
    await h.answer("Действие отменено")
    await h.get_data()
    h.messages.clear()
    h.quota = 0
    await h.update_data()

@router.message(F.text.startswith("/"))
async def cmd_cancel(message: types.Message, state:FSMContext):
    await message.answer("Команда не поддерживается")

@router.message(BotStates.api_key, F.text)
async def message_api_key(message: types.Message, state:FSMContext):
    h = gpt_helper(message, state)
    await h.save_api_key()
    text = bot_constants.api_key_saved
    await h.select_choice(BotStates.chatgpt, text)

@router.message(BotStates.chatgpt, F.text)
@router.message(F.text)
async def message_with_text(message: types.Message, state:FSMContext):
    h = gpt_helper(message, state)
    await h.answer_gpt()

