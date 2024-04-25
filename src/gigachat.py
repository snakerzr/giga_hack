import os

from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

CREDS = os.environ["CREDS"]

chat = GigaChat(credentials=CREDS, scope="GIGACHAT_API_CORP", verify_ssl_certs=False)


def compare_summarize(old_article, new_article, system_message, instruction):
    if not system_message:
        system_message = "Ты юрист, который хорошо разбирается в текстах законов."

    if not instruction:
        instruction = f"""
Привет! Сравни две итерации фрагмента закона и опиши юридическим языком коротко тезисно изменения:
Старая версия закона: {old_article}
Новая версия закона: {new_article}
ОЧЕНЬ КОРОТКО, МАЛО СЛОВ, КРАТКО ОБОБЩИ
    """.strip()

    messages = [SystemMessage(content=system_message)]
    messages.append(HumanMessage(content=instruction))

    res = chat(messages)

    return res.content


def generate_analysis(query, expertise, system_message, instruction):
    if not system_message:
        system_message = "Ты юрист, который хорошо разбирается в текстах законов."

    if not instruction:
        instruction = f"""
Напиши экспертно-правовой комментарий об изменениях в статье закона, основываясь на выдержках из научной работы.
Изменения в законе: {query}
Выдержки из научной работы: {expertise}
В ответе делай отсылку к научной работе. Ответ юридическим языком:""".strip()
    messages = [SystemMessage(content=system_message)]
    messages.append(HumanMessage(content=instruction))

    res = chat(messages)
    return res.content
