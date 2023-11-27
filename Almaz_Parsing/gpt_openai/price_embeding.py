from gpt_openai.gptfunc_a import *
from parsing.conf import config
import os 
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
# Инициализирум модель эмбеддингов

from openai import AsyncOpenAI

gpt = gptfunc_a_class()
# os.path.dirname(config.data_path)
class price_embeding_class:
    def load_from_md(self):
        self.filename = config.data_path+"/price.md"

        self.docs =[]
        with open(self.filename,"r", encoding="utf-8") as f:
            txt = f.read()
            self.docs.append(txt)

        self.fragments = gpt.split_text(self.docs)

        from langchain.docstore.document import Document
        def func(f:Document):
            h1 = f.metadata["H1"]
            h2 = f.metadata["H2"]
            # content =f.page_content
            d= Document(page_content=f"Price. {h1}\n{h2}",metadata=f.metadata)
            return d

        self.price_fragments = [func(f)  for f in self.fragments]


        # Создадим индексную базу из разделенных фрагментов текста
        self.init_openai()
        self.db = FAISS.from_documents(self.price_fragments, self.embeddings)

        self.db.save_local(self.db_filename)
    def init_openai(self):
        self.client =AsyncOpenAI(api_key=config.OPENAI_API_KEY)
        self.embeddings = OpenAIEmbeddings(async_client=self.client, openai_api_key=config.OPENAI_API_KEY)

    def load(self):
        self.db_filename = config.data_path+"/price_db"
        if not os.path.exists(self.db_filename):
            self.load_from_md()
        else:
            self.init_openai()
            self.db = FAISS.load_local(self.db_filename, self.embeddings)
            

price_db = price_embeding_class()
price_db.load()
