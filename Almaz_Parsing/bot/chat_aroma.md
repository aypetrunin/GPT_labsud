import re
from aiogram.types import Message
from aiogram import Router, F

import app.gpt
import database.requests as db_req
from app.keyboard import create_rating_keyboard

router_chat = Router()

@router_chat.message(F.text == '/start')
async def cmd_start(msg: Message):
    user_id = msg.from_user.id
    username = msg.from_user.username
    chat_id = msg.chat.id
    message_id = msg.message_id

    await new_message(message_id, chat_id, user_id, '/start', username)
    text_answer = await db_req.official_text_messages('start')
    sent_message=await msg.answer(text_answer)
    message_id = sent_message.message_id
    await db_req.add_or_update_message(message_id, chat_id, user_id, text_answer, username, type_message='text',
                                       role='assistant', model_bot='official'
                                       )

# не текстовое сообщение
@router_chat.message(~F.text)
async def non_text_message_handler(msg: Message):
    user_id = msg.from_user.id
    username = msg.from_user.username
    chat_id = msg.chat.id
    message_id = msg.message_id

    await new_message(message_id, chat_id, user_id, 'non_text_message', username)
    text_answer = await db_req.official_text_messages('non_text_message')
    sent_message = await msg.answer(text_answer)
    message_id = sent_message.message_id
    await db_req.add_or_update_message(message_id, chat_id, user_id, text_answer, username, type_message='non_text_message',
                                       role='assistant', model_bot='official'
                                    )

@router_chat.message(F.text)
async def text_message_handler(msg: Message):
    text = msg.text or msg.caption   # Проверяем, есть ли текст в сообщении
    user_id = msg.from_user.id
    username = msg.from_user.username
    chat_id = msg.chat.id
    message_id = msg.message_id
    if text and not re.search_with_score('[a-zA-Zа-яА-Я0-9]', text):
        await new_message(message_id, chat_id, user_id, 'non_text_message', username)
        text_answer = await db_req.official_text_messages('non_text_message')
        answer_message = await msg.answer(text_answer)
        answer_message_id = answer_message.message_id
        await db_req.add_or_update_message(answer_message_id, chat_id, user_id, text_answer, username,
                                           type_message='non_text_message',
                                           role='assistant', model_bot='official'
                                           )
    else:
        await new_message(message_id, chat_id, user_id, text, username)
        text_pause = await db_req.official_text_messages('pause')
        # pause_message = await msg.answer(text_pause)
        (topic, topic_message) = await app.gpt.gpt_GPT_consultant(msg, user_id, text, text_pause)
        #topic_message = await msg.answer(topic)

        topic_message_id = topic_message.message_id
        await db_req.add_or_update_message(topic_message_id, chat_id, user_id, topic, username,
                                           type_message='GPT',role='assistant', model_bot='GPT_consultant'
                                           )

        await db_req.add_rating(message_id, chat_id, user_id, text,topic_message_id, topic)
        rating_id =await db_req.find_rating_id_by_question(message_id, chat_id)
        print( rating_id)

        text_keyboard= await db_req.official_text_messages('text_keyboard')
        keyboard_message = await msg.answer(text_keyboard, reply_markup=create_rating_keyboard(msg.chat.id, 0, rating_id))
        keyboard_message_id = keyboard_message.message_id
        # Создаем новую клавиатуру с корректными данными
        new_keyboard = create_rating_keyboard(msg.chat.id, keyboard_message_id , rating_id)
        print(msg.chat.id, keyboard_message_id , rating_id)
        # Обновляем клавиатуру в отправленном сообщении
        await keyboard_message.edit_reply_markup(reply_markup=new_keyboard)



async def new_message(telegram_id, chat_id, user_id, message, username=None):
    try:
        await new_user(user_id, username)
        await db_req.add_or_update_message(telegram_id, chat_id, user_id, message, username, type_message='text',
                                               role='user', model_bot='user'
                                               )

    except Exception as e:
            await db_req.log_error(
                function_name="manage_message_processing",
                arguments=(f"telegram_id: {telegram_id}, chat_id: {chat_id}, user_id: {user_id},"
                       f" message: {message}, username: {username}"
                       ),
            error_message=str(e)
            )


    return

async def new_user(user_id, username=None):
    try:
        current_user_id = await db_req.find_user_by_id(user_id)
        if current_user_id:
            return
        else:
            # Если user_id не существует в базе данных, добавляем нового пользователя и сообщение
            await db_req.add_user(user_id, username)
    except Exception as e:
            await db_req.log_error(
                function_name="new_user",
                arguments=(f" user_id: {user_id}, username: {username}"),error_message=str(e)
            )
    return