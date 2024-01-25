# Запуск проекта

1. Создать файл .env и прописать переменные
2. создаем виртуальное окружение virtualenv env
переключаемся на него env/scripts/activate
устанавливаем зависимости pip install -r requirements.txt
3. загружаем индексную БД python -m gptindex.check_ix 
4. создаем БД и проверяем ее работоспособность
    python -m db.check_db
5. запускаем бота
    python -m main_bot
Если надо пересоздать БД, можно её просто удалить

# Настройка переменных
.env
1. TG_BOT_TOKEN
OPENAI_API_KEY= "sk-QW6yd17p3pC1qHEdcpBa*****"
TG_TOKEN = "*****"
2. Путь и подключение к БД
database_path = "sqlite+aiosqlite:///c:/Data/DB/sqlite3/db_stag_labsud.sqlite3"
3. Путь для хранения индексной БД
index_path = "c:/Data/DB/index/labsud"

## ixconfig.py
содержит от куда надо загружать индексные БД

# API
1. Реализовать FastAPI
2. Запуск АПИ
uvicorn start_api:app --reload
3. использование АПИ
смотри api/readme.md
    test/test_api.ipynb
4. 
# План для разработки
1. скачиваем и загружаем индексную БД gptindex.gptutils
2. создаем бота и подгружаем базу
3. подключаю бд для логирования запросов
4. подключаю логер и через него веду логи
5. подключаю выгрузку в эксель

зафиксировать библиотеки
pip freeze > requirements.txt
# Bot
https://t.me/AlmazLabSudbot
start - Start
dialog - включить режим диалога
nodialog - Выключить режим диалога 
clear - Очистить историю диалога 
api_key - Подключить свой ключ API
status - Показать статус запросов

# Примеры вопросов
Где можно к вам обратиться?
Автотехническая экспертиза

# Инструкции
Видео с описанием
https://youtu.be/vxgCiUNTO8A
