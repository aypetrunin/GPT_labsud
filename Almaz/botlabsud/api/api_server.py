from fastapi import FastAPI, HTTPException
import requests
import json
from pydantic import BaseModel
from datetime import datetime
from utils.initconf_env import config
from utils.logger import logger
logger.info("Загружаем БД")

from db.base import init_database
init_database(config.database_path)
logger.info("Start. Загружаем индексную БД")

from gptindex.ixapp import ixapp
import asyncio

ixapp.init()
from db.base import database
from api.api_gpt import Gpt_helper
from db.dbrequests import RequestsDB as RequestsDB
logger.info("Start.")

# класс с типами данных параметров
class Item(BaseModel):
    user_id: str
    text: str
    dialog: int

# создаем объект приложения
app = FastAPI()


# функция обработки get запроса + декоратор
@app.get("/")
def read_root():
    return {"message": "answer"}


requestcount = 0
requestPerHour = {} # {8:12,9:1, 10:15}
requestPerHourList = []
class ItemHourRequest:
    def __init__(self):
        self.start_dt = datetime.now()
        self.count = 0

data = {}

@app.get("/requestcount")
def get_requestcount():
    return requestcount


@app.get("/requestperhour")
def get_requestperhour():
    return requestPerHour

@app.get("/requestperhourlist")
def get_requestperhourlist():
    return requestPerHourList

async def get_gpt_helper(user_id:str, text:str):
    h = Gpt_helper(text)
    if user_id in data:
        db:RequestsDB = data[user_id]
        db.open()
        await h.get_data(db, False)
    else:
        db = RequestsDB()
        db.user_api_id = user_id
        await h.get_data(db)
    print(h)
    return h

def update_requestcount():
    global requestcount
    requestcount +=1
    global requestPerHour
    x = datetime.now()
    hour = x.hour
    if not hour in requestPerHour:
        i = ItemHourRequest()
        requestPerHour[hour]=i
        requestPerHourList.append(i)
    else:
        i = requestPerHour[hour]
        if i.start_dt.day<x.day:
            i = ItemHourRequest()
            requestPerHour[hour] = i
            requestPerHourList.append(i)
    i.count+=1

# функция обработки post запроса + декоратор
@app.post("/api/get_answer")
async def get_answer(question: Item):
    # try:
        update_requestcount()
        h:Gpt_helper = await get_gpt_helper(question.user_id, question.text)
        h.data.dialog = question.dialog
        answer = await h.answer_gpt()
        await h.close()
        return answer
    # except json.JSONDecodeError:
    #     raise HTTPException(status_code=400, detail="Invalid JSON format in the request body")
    # except requests.RequestException as e:
    #     raise HTTPException(status_code=500, detail=f"Error connecting to OpenAI API: {str(e)}")
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/api/add_rating")
async def get_answer(rate:int, message_id:int):
    update_requestcount()
    h:Gpt_helper = await get_gpt_helper(0, "")
    print("rate", rate)
    h.db.usermessage_id = message_id
    await h.db.add_rating(rate)
    await h.close()
    return f"ok {rate}"
