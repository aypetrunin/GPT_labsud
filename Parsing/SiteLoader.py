from bs4 import BeautifulSoup
import os

url = "https://federallab.ru"
url_site_map = f'{url}/sitemap.xml'
path_content = "data"

def readFile(num):
    filename = f'{path_content}/{num}.html'
    with open(filename,"r",encoding="utf-8") as f:
        text = f.read()    
    return text

def readPages():
    if not os.path.exists(path_content):
        os.mkdir(path_content)
    filename = f'{path_content}/pages.txt'
    with open(filename,"r", encoding="utf-8") as f:
        pages = f.read()
    pages = pages.split()
    return pages

def saveDocs(docs):
    for i, e in enumerate(docs):
        num = str(i).rjust(2,"0")
        filename = f'{path_content}/{num}.html'
        if not os.path.exists(filename):
            with open(filename,"w", encoding="utf-8") as f:
                f.write(str(e))

def parseAll():
    pages = readPages()
    for i, e in enumerate(pages):
        num = str(i).rjust(2,"0")
        filename = f'{path_content}/{num}.md'
        if not os.path.exists(filename):
            sl = SiteLoader(num)                
            sl.parse()
            sl.save()

class SiteLoader():
    def __init__(self, num) -> None:
        self.num=num
        self.lines=[]

    def page_avto_expert_wr(self, els):
        lines = self.lines
        for el in els[0].childGenerator():
            #print(str(el))
            if el.name=="div":
                if "class" in el.attrs:
                    c = el.attrs["class"]
                    if c==["avt_top_text"]:
                        t= el.text
                        lines.append(t)
                    elif c ==["avt_why"]:
                        h2 = el.h2
                        if h2!=None:
                            lines.append("## "+h2.text)
                        lines.extend(map(lambda x:x.text, el.findAll("p")))
                    elif c==["avt_list"]:
                        h3= el.h3
                        if h3!=None:
                            lines.append("## "+h3.text)
                        ol = el.ol
                        if ol!=None:
                            lines.append(ol.text)
                else:
                    lines.append("# Table")
                    h2 = el.h2
                    if h2!=None:
                        lines.append("## "+h2.text)
                    table = el.table
                    if table!=None:
                        lines.append(str(table))

    def page_text(self, els):
        lines = self.lines
        for el in els.childGenerator():
            #print(str(el))
            if el.name=="p":
                lines.append("")
                lines.append(el.text)
            elif el.name =="h2":
                lines.append("## "+el.text)
            elif el.name =="h3":
                lines.append("## "+el.text)
            elif el.name == "table":
                lines.append("# Table")
                lines.append(str(el))
            elif el.name =="ol":
                lines.append(el.text)
            elif el.name =="div":
                self.page_text(el)

    def parse(self):
        filename = f'{path_content}/{self.num}.html'
        with open(filename,"r",encoding="utf-8") as f:
            text = f.read()
        soup = BeautifulSoup(text, "html.parser" )
        content = soup.findAll('div', class_="page_content")
        if len(content)==0:
            return
        self.lines = []
        self.lines.append("# "+ content[0].h1.text)
        els = content[0].findAll('div', class_="page_avto_expert_wr")
        if len(els)==0:
            els2 = content[0].findAll('div', class_="page_text")
            if (len(els2))>0:
                self.page_text(els2[0])
            else:
                self.page_text(content[0])
        else:
            self.page_avto_expert_wr(els)
            #print(self.lines)
        return 

    def save(self):
        text = "\n".join(self.lines)
        filename = f'{path_content}/{self.num}.md'
        with open(filename,"w",encoding="utf-8") as f:
            f.write(text)
