import htmlLoader
htmlLoader.reloadhtml()

from SiteLoader import *
p = dpages[57]

text ="\n"
with open(p.mdfile(),"r") as f:
    text += f.read()

db = text.split('\n# ')

dbT=[]
fTable = "Table\n"
for i in db:
    if i.startswith(fTable):
        dbT.append(i[len(fTable):])

from conf import config
import json
filename = config.data_path+"/tables.html"
with open(filename,"w",encoding="utf-8") as f:
    json.dump(dbT,f)


#with open(filename,"r",encoding="utf-8") as f:
#    obj = json.load(f)

from tabletomd import table_to_md

table_to_md()
