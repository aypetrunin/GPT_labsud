from  openai import AsyncOpenAI
from db.dbrequests import RequestsDB, RequestsDBData
from utils.logger import logger
from datetime import datetime
from config import config
from gptindex.ixapp import ixapp
from gptindex.gptutils import num_tokens_from_string

class Gpt_helper:
    prompt_tokens=0
    completion_tokens=0
    def __init__(self, query:str):
        self.query = query
        self.context_data = None
        self.api_key = None
        self.clientOpenAI =None
        self.quota = 0
        self.api_key = None
        self.q_tokens = 0
        self.a_tokens = 0
        self.data:RequestsDBData = None
        self.db:RequestsDB = None #RequestsDB(self.message)
        self.d1 = datetime.now()

    async def close(self):
        await self.db.close()
    async def get_data(self, db:RequestsDB = None, update = True):
        if db:
            self.db = db
        else:
            self.db= RequestsDB()
        self.data = self.db.data
        if update:
            await self.db.update_apiuser()

    async def update_data(self):
        await self.db.update_data()

    def ClientAI(self):
        api_key = config.OPENAI_API_KEY
        if not self.clientOpenAI:
            self.clientOpenAI = AsyncOpenAI(api_key=api_key)
        return self.clientOpenAI

    async def query_refiner(self,  query):
        config = ixapp.config
        model = config.openai_model
        client:AsyncOpenAI = self.ClientAI()
        conversation = self.conversation_string( self.data.messages, config.dialog_depth)
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system",
                 "content": config.refiner_prompt.format(conversation= conversation, query = query)},
                {"role": "user", "content": f"{query}"}
            ],
            temperature=0)
        u = response.usage
        self.prompt_tokens += u.prompt_tokens
        self.completion_tokens += u.completion_tokens
        return str(response.choices[0].message.content)

    def conversation_string(self, messages, dialog_depth):
        conversation_string = ''
        k = 0 if len(messages) <= dialog_depth * \
                 2 else -1 * dialog_depth * 2
        for message in messages[k:]:
            conversation_string += f"{message['role']}: {message['content']}\n"
        return conversation_string

    async def completion(self, usercontent, refined_query):
        client: AsyncOpenAI = self.ClientAI()
        config = ixapp.config
        stream = config.stream
        full_response = ""
        if config.testing:
            full_response = "Ответ системы"
        else:
            usercontent = f"Документ с информацией для ответа пользователю:\n {usercontent}.\nВопрос клиента: {refined_query}"
            responses = await client.chat.completions.create(
                model=config.openai_model,
                messages=[
                    {"role": "system", "content": ixapp.promt},
                    {"role": "user",
                     "content": usercontent}
                ],
                temperature=0,
                stream=stream,
            )
            if stream:
                async for response in responses:
                    delta = (response.choices[0].delta.content or "")
                    if len(delta) > 0:
                        full_response += delta
                        await self.edit_text(full_response + "▌", wait=True)
                self.prompt_tokens += num_tokens_from_string(ixapp.promt + usercontent + 6)
                self.completion_tokens += num_tokens_from_string(full_response)
            else:
                full_response = responses.choices[0].message.content
                usage = responses.usage
                self.prompt_tokens += usage.prompt_tokens
                self.completion_tokens += usage.completion_tokens

        # await self.edit_text_rating(text=full_response)
        await self.db.answer_usermessage(0, full_response, self.prompt_tokens,
                                         self.completion_tokens)
        # await self.print_usage_tokens()
        return full_response

    async def answer_gpt(self):
        await self.db.new_usermessage(self.query)
        h = self
        # if not await self.check_quota():
        #     return
        # await h.pause()
        refined_query = self.query
        try:
            is_query, db_response = ixapp.find_query(h.query)
            logger.debug(f"Вопрос: {h.query}  Dialog {h.data.dialog}")
            if h.data.dialog == 0:
                h.data.messages = []
            if not is_query:
                # Формирование уточняющего вопроса по диалогу.
                if len(h.data.messages) > 1:
                    # await h.edit_text("Уточняю вопрос...")
                    refined_query = await h.query_refiner(h.query)
                    logger.debug(f"refined_query: {refined_query}")
                    # await h.edit_text(f"Отвечаю на вопрос: {refined_query}")
                else:
                    refined_query = h.query
                h.data.messages.append({"role": "user", "content": f"{h.query} ({refined_query})"})
                # Возвращение релевантных документов по запросу.
                content = ixapp.bd_retriever(refined_query)
                full_response = await h.completion(content, refined_query)
                text = full_response
                logger.debug("Ответ: "+full_response)
                h.data.messages.append({"role": "assistant", "content": f"{h.query} ({full_response})"})
            else:
                text = f"(ответ из базы вопросов)\n{db_response}"
                logger.debug(text)
                await self.db.answer_usermessage( 0, text, self.prompt_tokens, self.completion_tokens)
                h.data.messages.append(
                    {"role": "user", "content": f"{h.query}"})
                h.data.messages.append(
                    {"role": "assistant", "content": db_response})
            await h.update_data()
        except Exception as e:
            text = "Ошибка: "+str(e)
            logger.exception("answer_gpt")
            # await h.answer(text)
            await self.log("answer_gpt", "", "Ошибка: "+text)
        d2 = datetime.now()
        sec = (d2 - self.d1).total_seconds()

        r = {"message": text,
             "message_id": h.db.usermessage_id,
             "prompt_tokens": h.prompt_tokens,
             "completion_tokens": h.completion_tokens,
             "refined_query": refined_query,
             "duration": str(sec),
             "question_db": is_query}
        return r
    async def log(self, func, param, text):
        await self.db.add_log(func, param, text)

