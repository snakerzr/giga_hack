import os

from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

CREDS = os.environ["CREDS"]

chat = GigaChat(credentials=CREDS, scope="GIGACHAT_API_CORP", verify_ssl_certs=False)


def compare_summarize(old_article, new_article, system_message, instruction):
    if not system_message:
        system_message = "Ты - квалифицированный юрист, который умеет анализировать статьи законов и внесенные в них изменения."

    if not instruction:
        instruction = """Сравни две редакции одной и той же статьи закона, принятые в разное время, и прокомментируй, используя юридическую терминологию, в чем состояли изменения.
Старая версия закона: {old_article}
Новая версия закона: {new_article}
Суммаризируй ответ, опиши только значимые изменения, кратко.""".strip()

    messages = [SystemMessage(content=system_message)]
    messages.append(
        HumanMessage(
            content=instruction.format(old_article=old_article, new_article=new_article)
        )
    )

    res = chat(messages)

    return res.content


async def abatch_compare_summarize(
    old_articles: list,
    new_articles: list,
    system_message=None,
    instruction_template=None,
):
    if not system_message:
        system_message = "Ты - квалифицированный юрист, который умеет анализировать статьи законов и внесенные в них изменения."

    if not instruction_template:
        instruction_template = """Сравни две редакции одной и той же статьи закона, принятые в разное время, и прокомментируй, используя юридическую терминологию, в чем состояли изменения.
Старая версия закона: {old_article}
Новая версия закона: {new_article}
Суммаризируй ответ, опиши только значимые изменения, кратко.""".strip()

    messages_batch = []
    for old_article, new_article in zip(old_articles, new_articles):
        instruction = instruction_template.format(
            old_article=old_article, new_article=new_article
        )
        messages_pair = [
            SystemMessage(content=system_message),
            HumanMessage(content=instruction),
        ]
        messages_batch.extend(messages_pair)

    res = await chat.abatch(messages_batch)

    return res


def generate_analysis(query, expertise, system_message, instruction):
    if not system_message:
        system_message = "Ты - квалифицированный юрист, который умеет анализировать статьи законов и внесенные в них изменения."

    if not instruction:
        instruction = """
Напиши экспертно-правовой комментарий об изменениях в статье закона, основываясь на выдержках из научной работы.
Изменения в законе: {query}
Выдержки из научной работы: {expertise}
В ответе делай отсылку к научной работе. Ответ юридическим языком:""".strip()
    messages = [SystemMessage(content=system_message)]
    messages.append(
        HumanMessage(content=instruction.format(query=query, expertise=expertise))
    )

    res = chat(messages)
    return res.content
