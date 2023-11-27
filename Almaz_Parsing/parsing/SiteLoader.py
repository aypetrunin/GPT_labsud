from bs4 import BeautifulSoup
import os
from parsing.conf import config

url = "https://federallab.ru"
url_site_map = f'{url}/sitemap.xml'
path_content = config.data_path

def readFile(num):
    name = dpages[num]
    filename = f'{path_content}/html/{name}.html'
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
        # num = str(i).rjust(2,"0")
        num = dpages[i] #str(i).rjust(2,"0")
        filename = f'{path_content}/html/{num}.html'
        if not os.path.exists(filename):
            with open(filename,"w", encoding="utf-8") as f:
                f.write(str(e))

def saveDocs_toload(docs, docstoload):
    for i, e in enumerate(docs):
        # num = str(i).rjust(2,"0")
        num = docstoload[i] #str(i).rjust(2,"0")
        filename = f'{path_content}/html/{num}.html'
        if not os.path.exists(filename):
            with open(filename,"w", encoding="utf-8") as f:
                f.write(str(e))


def parseAll():
    pages = readPages()
    for i, e in enumerate(pages):
        num = dpages[i] #str(i).rjust(2,"0")
        filename = num.mdfile()
        if not os.path.exists(filename):
            sl = SiteLoader(num)                
            sl.parse()
            sl.save()

def list_docs_toload():
    liPages = []
    for i in dpages:
        num = dpages[i] #str(i).rjust(2,"0")
        if not os.path.exists(num.htmlfile()):
           liPages.append(num)
    return liPages

import re
class FileItem:
    def __init__(self, page, num) -> None:
        self.page=page
        self.num = str(num).rjust(2,"0")
        m=re.search(r'/([a-zA-Z0-9-_()]+)/$',page)
        v=None
        if m!=None:
            v = m.group(1)
        self.name = v
        pass
    def __str__(self) -> str:
        return f'{self.num}-{self.name}'
        pass
    def htmlfile(self):
        return f'{path_content}/html/{self}.html'
    def mdfile(self):
        return f'{path_content}/md/{self}.md'

def PagesToDict(pages):
    dpages = dict()
    for i,p in enumerate(pages):
        it = FileItem(p,i)
        if it.name==None:
            print(it)
        dpages[i]=it
    return dpages


pages = readPages()
dpages = PagesToDict(pages)

import shutil
def  MoveFiles(dirname, dpages, ext="md"):
    # ext ="html"
    # ext ="md"
    path_content = dirname +"/"+ext
    if not os.path.exists(path_content):
        os.mkdir(path_content)
    for i in dpages:
        p= dpages[i]
        s1=f'{dirname}/{p.num}.{ext}'
        s2=f'{dirname}/{ext}/{p}.{ext}'
        if os.path.exists(s1):
            shutil.move(s1,s2)

class SiteLoader():
    def __init__(self, num) -> None:
        self.num=num
        self.name = dpages[self.num]
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
        filename = f'{path_content}/html/{self.name}.html'
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
        filename = f'{path_content}/md/{self.name}.md'
        with open(filename,"w",encoding="utf-8") as f:
            f.write(text)
