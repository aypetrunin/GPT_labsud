# преобразование таблицы json в md для деления на чанки

import json
from parsing.tableLoader import TableLoader
from parsing.conf import config

class table_do_md_class:

    def load(self):
        self.filename = config.data_path+"/tables.html"
        with open(self.filename,"r",encoding="utf-8") as f:
            self.obj = json.load(f)

        self.t1 = TableLoader(self.obj[0])
        self.t2 = TableLoader(self.obj[1])

    def parse_t1(self):
        self.t1.parseHeader()
        self.t1.parseBody()
        for b in self.t1.body:
            b.parseBody()
        #self.save(self.t1,"price.md")


    def save(self,t1,filename="price.md"):
        h = t1.header
        t =[]
        for b in t1.body:
            t.append("# "+ b.name)
            for ta in b.table:
                t2 = ta[0][0]
                if t2=="":
                    t2 = ta[0][1]
                    #print( t2)
                t.append("## "+t2)
                d = {'header':h, 'body':ta}
                txt = json.dumps( d, ensure_ascii=False)
                t.append(txt)
        # сохранить текст в файл
        fielname =config.data_path+"/"+filename
        with open(fielname,"w") as f:
            f.write("\n".join(t))

    def parse_t2(self):
        self.t2.parseHeader2()
        self.t2.parseBody2()    
        for b in self.t2.body:
            b.parseBody()
        #self.save(self.t2,"price2.md")

