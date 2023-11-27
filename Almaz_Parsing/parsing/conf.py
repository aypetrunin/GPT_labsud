import json
import os
from pprint import pprint

filename = ".confjson"
config_json = {
    'TG_TOKEN':"",
    'OPENAI_API_KEY':"",
    "database_path" :'sqlite:///c:/Data/DB/sqlite3/db_stag_labsud.sqlite3',
    "config_file_path" :  "c:/Data/DB/config/stag_labsud_config.json",
    "data_path" : "c:/Data/Study/NU/Stag/py/"
}
# 'database_path': 'sqlite+aiosqlite:///c:/Data/DB/sqlite3/db_bot_aroma.sqlite3'
# aiosqlite - библиотека для ассинхронных вызовов
# sqlite+aiosqlite

def load_config(filename):
    global config_json
    if not os.path.exists(filename):
        with open(filename,"w") as f:
            json.dump(config_json, f, ensure_ascii=False, sort_keys=True)
    else:
        with open(filename,"r") as f:
            config_json = json.load(f)

load_config(filename)
if config_json["config_file_path"]:
    load_config(config_json["config_file_path"])

class config_class:
    TG_TOKEN =""
    OPENAI_API_KEY =""
    database_path = ''
    config_file_path = ""
    data_path =""

config = config_class()
config.TG_TOKEN = config_json["TG_TOKEN"]
config.OPENAI_API_KEY = config_json["OPENAI_API_KEY"]
config.database_path = config_json["database_path"]
config.config_file_path = config_json["config_file_path"]
config.data_path = config_json["data_path"]
os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY

if __name__ == '__main__':
  pprint(config_json)

