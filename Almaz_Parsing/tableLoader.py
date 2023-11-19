# преобразование таблицы html в json

from bs4 import BeautifulSoup
import json

class TableGroup:
    '''Разделы таблицы'''
    def __init__(self, name) -> None:
        self.name=name
        self.body = []
        self.table =[]
        pass
    def __str__(self) -> str:
        return self.name
        pass

    def parseBody(self):
        trs = self.body
        self.table =[]
        for tr in trs:
            tds = tr.find_all('td')
            detail = []
            td0 = tds[0]
            ps = td0.find_all("p")
            if len(ps)>1:
                for p in ps:
                    txt =p.text.strip()
                    if txt!="":
                        detail.append( [txt])
                for i in range(1,len(tds)):
                    td=tds[i]
                    ps = td.find_all("p")
                    if len(ps)==1:
                        txt =ps[0].text.strip()
                        for j in range(1,len(detail)):
                            detail[j].append(txt)
                    else:
                        j=1
                        for p in ps:
                            txt = p.text.strip()
                            if txt!="":
                                detail[j].append(txt)
                                j+=1
            elif len(ps)==1:
                txt = ps[0].text.strip()
                detail.append( [txt])
                for i in range(1,len(tds)):
                    td=tds[i]
                    ps = td.find_all("p")
                    if len(ps)>=1:
                        txt =ps[0].text.strip()
                        detail.append(txt)

            self.table.append(detail)


        

class TableLoader:
    '''преобразование таблицы html в json'''
    def __init__(self, html_table) -> None:
        self.html_table = html_table
        self.soup = BeautifulSoup(html_table, 'html.parser')
        self.tables = self.soup.find_all('table')
        if len(self.tables)>0:
            self.table = self.tables[0]
            self.thead = self.table.find_all('thead')
            self.tbody = self.table.find_all('tbody')
        self.header =[] 
    def parseHeader(self):
        '''в заголовке таблицы 1 строка
        '''
        self.header =[] 
        headers_trs = self.thead[0].find_all('tr')
        if len(headers_trs)==1:
            tr = headers_trs[0]
            for td in tr.find_all('td'):
                txt = td.text.replace("\n","")
                self.header.append(txt)
        return self.header

    def parseHeader2(self):
        '''в заголовке таблицы 2 строки и есть объединение ячеек
        '''
        self.header =[] 
        headers_trs = self.thead[0].find_all('tr')
        h =[]
        h2=[]
        tr = headers_trs[0]
        for td in tr.find_all('td'):
            txt = td.text.replace("\n","")
            h.append(txt)
            if td.has_attr("colspan"):
                for j in range(1, int(td["colspan"])):
                    txt = td.text.replace("\n","")
                    h.append(txt)
            if td.has_attr("rowspan"):
                rs =int(td["rowspan"])
                if rs>1:
                    for j in range(1, rs):
                        h2.append("")
        tr = headers_trs[1]
        for td in tr.find_all('td'):
            txt = td.text.replace("\n","")
            h2.append(txt)
        headers = list(zip(h, h2))
        def ff(x):
            if x[1]=="":
                return x[0]
            else:
                return "\n".join(x)
        self.header = list(map(ff, headers))

        return self.header


    def parseBody(self):
        self.body = []
        trs = self.tbody[0].find_all('tr')
        tg = None
        for tr in trs:
            tds = tr.find_all('td')
            if len(tds)==1:
                td=tds[0]
                ps = td.find_all('p')
                txt = "\n".join([p.text for p in ps])
                tg = TableGroup( txt)
                self.body.append(tg)
            else:
                if (tg==None):
                    tg = TableGroup("")
                    self.body.append(tg)
                tg.body.append(tr)
                
    def parseBody2(self):
        self.body = []
        trs = self.tbody[0].find_all('tr')
        tg = None
        for tr in trs:
            tds = tr.find_all('td')
            if len(tds)==1:
                td=tds[0]
                ps = td.find_all('p')
                txt = "\n".join([p.text for p in ps])
                tg = TableGroup( txt)
                self.body.append(tg)
            elif len(tds)==2:
                td=tds[0]
                ps = td.find_all('p')
                ps2 = tds[1].find_all('p')
                ps.extend(ps2)
                txt = " ".join([p.text for p in ps])
                tg = TableGroup( txt)
                self.body.append(tg)
            else:
                if (tg==None):
                    tg = TableGroup("")
                    self.body.append(tg)
                tg.body.append(tr)




def html_table_to_json(html_table):
    soup = BeautifulSoup(html_table, 'html.parser')

    headers_trs = soup.find_all('tr', {'class': 'table-header_blue'})
    tr = headers_trs[0]
    h = []
    h2 = []
    for td in tr.find_all('td'):
        h.append(td.text)
        if td.has_attr("colspan"):
            for j in range(1, int(td["colspan"])):
                h.append(td.text)
        if td.has_attr("rowspan"):
            rs =int(td["rowspan"])
            if rs>1:
                for j in range(1, rs):
                    h2.append("")
    tr = headers_trs[1]

    for td in tr.find_all('td'):
        h2.append(td.text)
    
    # Combine multi-level headers
    headers = list(zip(h, h2))
    print(headers)

    rows = soup.find_all('tr')
    table_data = []
    for row in rows:
        if  "class" in row.attrs:
            continue
        cells = row.find_all('td')
        row_data = dict(zip(headers, [cell.text for cell in cells]))
        table_data.append(row_data)

    #return json.dumps(table_data, indent=4, ensure_ascii=False)
    print(table_data)

# html_table = html_string
# html_table_to_json(html_table)
#print(html_table_to_json(html_table))