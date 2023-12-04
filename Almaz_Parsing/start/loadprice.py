# Обработчик для обработки таблиц с ценами
from start.htmlLoader import reloadhtml
reloadhtml()

from parsing.SiteLoader import *
p = dpages[57]

text ="\n"
with open(p.md_file(), "r") as f:
    text += f.read()

db = text.split('\n# ')

dbT=[]
fTable = "Table\n"
for i in db:
    if i.startswith(fTable):
        dbT.append(i[len(fTable):])

from parsing.conf import config
import json
filename = config.data_path+"/tables.html"
with open(filename,"w",encoding="utf-8") as f:
    json.dump(dbT,f)


#with open(filename,"r",encoding="utf-8") as f:
#    obj = json.load_db_price_old(f)

from parsing.tabletomd import table_do_md_class
m = table_do_md_class()
m.load()

m.parse_t1()
m.save(m.t1,"price.md")

m.parse_t2()
m.save(m.t2,"price.md")

