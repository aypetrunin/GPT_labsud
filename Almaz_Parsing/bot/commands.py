from bot.bot import router_chat as router, BotStates
from aiogram import filters, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@router.message(filters.Command("start"))
async def cmd_start(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    menu_button = InlineKeyboardButton('Menu', callback_data='menu')
    keyboard.add(menu_button)

    await message.answer(
        """Здравствуйте я нейроконсультант ФЛСЭ 
        чтобы узнать цены введите команду /price
        чтобы получить консультацию по услугам команда /uslugi
        """, reply_markup=keyboard
    )


@router.callback_query(lambda c: c.data.startswith("menu"))
async def handle_callback(callback_query: types.CallbackQuery):
    if callback_query.data == 'menu':
        keyboard = InlineKeyboardMarkup(row_width=1)
        button1 = InlineKeyboardButton('Option 1', callback_data='option1')
        button2 = InlineKeyboardButton('Option 2', callback_data='option2')
        keyboard.add(button1, button2)

        await callback_query.message.bot.edit_message_text(
                                    text="Menu:",
                                    reply_markup=keyboard)


@router.message(filters.Command("price"))
async def cmd_price(message: types.Message, state: FSMContext):
    await message.answer(
        """По какой услуге вы хотите узнать стоимость?""",
    )
    await state.set_state(BotStates.price)


@router.message(filters.Command("uslugi"))
async def cmd_price(message: types.Message, state: FSMContext):
    await message.answer(
        """По какой услуге вы хотите получить консультацию?""",
    )
    await state.set_state(BotStates.price)


@router.message(filters.Command(commands=["cancel"]))
@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=types.ReplyKeyboardRemove()
    )
