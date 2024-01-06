import streamlit as st
import openai
import tiktoken
from openai import OpenAI
from utils import *


url_promt = "https://raw.githubusercontent.com/terrainternship/GPT_labsud/main/Galina/FLSE_promt"
url_bd = 'https://github.com/terrainternship/GPT_labsud/raw/main/federallab_bd_index_v2.zip'
url_question = 'https://github.com/terrainternship/GPT_labsud/raw/main/federallab_bd_question.zip'

dialog_depth = 2

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo-1106"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Наша фирма оказывает услуги по экспертизе и оценке. Чем могу я Вам помочь?"}]

if 'federallab_promt' not in st.session_state:
    st.session_state.federallab_promt = load_file(url_promt)
    print("Загрузка промта.")

if 'federallab_bd' not in st.session_state:
    st.session_state.federallab_bd = load_bd_vect(url_bd)
    print("Загрузка Базы знаний.")

if 'federallab_question' not in st.session_state:
    st.session_state.federallab_question = load_bd_question(url_question)
    print("Загрузка Базы вопрсов.")

with st.sidebar:
    openai_api_key = st.text_input(
        "OpenAI API Key", key="chatbot_api_key", type="password")
    st.divider()
    if st.button("Новый диалог", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Наша фирма оказывает услуги по экспертизе и оценке. Чем могу я Вам помочь?"}]
    st.divider()

# openai_api_key = st.secrets["OPENAI_API_KEY"]
clientOpenAI = OpenAI(api_key=openai_api_key)

with st.container():
    st.header("Нейро ассистент ФЛСЭ")
    stick_it_good()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Второй вапиант вывода сообщений в чат
# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])

if query := st.chat_input("Введите свой вопрос."):

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    with st.chat_message("user"):
        message_user = st.empty()
        message_user.markdown(query)

    with st.spinner('Думаю ...'):

        # Проверка вопроса на наличие в базе вопросов.
        is_query, bd_responce = find_query(
            st.session_state.federallab_question, query)

        if not is_query:
            # Формирование по диалогу уточняющего вопроса.
            if len(st.session_state.messages) > 1:
                refined_query = query_refiner(
                    client=clientOpenAI,
                    model=st.session_state["openai_model"],
                    conversation=conversation_string(
                        st.session_state.messages, dialog_depth),
                    query=query)
            else:
                refined_query = query

            # with st.chat_message("user"):
            message_user.markdown(f"{query} ({refined_query})")

            st.session_state.messages.append(
                {"role": "user", "content": f"{query} ({refined_query})"})

            # Возвращение релевантных документов по запросу.
            content = bd_retrever(
                st.session_state.federallab_bd, refined_query)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                for response in clientOpenAI.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=[
                        {"role": "system", "content": st.session_state.federallab_promt},
                        {"role": "user",   "content": f"Документ с информацией для ответа пользователю:\n {content}.\nВопрос клиента: {refined_query}"}
                    ],
                    temperature=0,
                    stream=True,
                ):
                    full_response += (response.choices[0].delta.content or "")
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response})
        else:
            message_user.markdown(f"{query} (ответ из базы вопросов)")
            st.chat_message("assistant").markdown(bd_responce)

            st.session_state.messages.append(
                {"role": "user", "content": f"{query} (ответ из базы вопросов)"})
            st.session_state.messages.append(
                {"role": "assistant", "content": bd_responce})
