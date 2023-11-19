# преобразование таблицы json в md для деления на чанки

import json
import tableLoader

def table_to_md():
    with open("data/tables.html","r",encoding="utf-8") as f:
        obj = json.load(f)

    t1 = tableLoader.TableLoader(obj[0])
    t2 = tableLoader.TableLoader(obj[1])

    t1.parseHeader()
    t1.parseBody()
    t2.parseHeader2()
    t2.parseBody2()    
    for b in t1.body:
        b.parseBody()
    for b in t2.body:
        b.parseBody()
    
    h = t1.header
    t =[]

    for b in t1.body:
        t.append("# "+ b.name)
        for ta in b.table:
            t.append("## "+ta[0][0])
            d = {'header':h, 'body':ta}
            txt = json.dumps( d, ensure_ascii=False)
            t.append(txt)

    # сохранить текст в файл
    fielname ="data/price.md"
    with open(fielname,"w") as f:
        f.write("\n".join(t))
