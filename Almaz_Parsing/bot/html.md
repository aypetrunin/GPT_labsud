
import telegram
from tabulate import tabulate

# Создайте объект Telegram Bot и укажите ваш токен
bot_token = 'YOUR_BOT_TOKEN'
bot = telegram.Bot(token=bot_token)

# Ваша таблица данных
data = [
    ['Name', 'Age', 'Location'],
    ['John', '25', 'New York'],
    ['Jane', '30', 'London'],
    ['Mike', '35', 'Paris']
]

# Преобразование таблицы данных в строку
table_str = tabulate(data, headers='firstrow')

# Отправка сообщения с таблицей в Telegram-бот
bot.send_message(chat_id='YOUR_CHAT_ID', text=table_str)



# html
import telegram

# Создайте объект Telegram Bot и укажите ваш токен
bot_token = 'YOUR_BOT_TOKEN'
bot = telegram.Bot(token=bot_token)

# Текст сообщения с форматированием HTML
message_text = '<b>Жирный текст</b>, <i>курсив</i>, <a href="http://example.com">ссылка</a>'

# Отправка сообщения с форматированием HTML
bot.send_message(chat_id='YOUR_CHAT_ID', text=message_text, parse_mode=telegram.ParseMode.HTML)

