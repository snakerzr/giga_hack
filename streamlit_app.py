import streamlit as st
from src.FAISS import faiss_db
from src.comparison import splitting_wrapped
from src.gigachat import compare_summarize, generate_analysis


def main():
    debug_mode = st.checkbox("DEBUG")
    st.title("Загрузка текстовых файлов")

    law_old = st.file_uploader("Загрузите старую редакцию", type=["txt"])
    law_actual = st.file_uploader("Загрузите новую редакцию", type=["txt"])
    if debug_mode:
        st.write("Ты юрист, который хорошо разбирается в текстах законов.")
        system_message_1 = st.text_input(
            "Введите системное сообщение для сравнения редакций:"
        )
        st.write("""
    Привет! Сравни две итерации фрагмента закона и опиши юридическим языком коротко тезисно изменения:
    Старая версия закона: {old_article}
    Новая версия закона: {new_article}
    ОЧЕНЬ КОРОТКО, МАЛО СЛОВ, КРАТКО ОБОБЩИ
        """)
        instruction_1 = st.text_input("Введите инструкцию для сравнения редакций:")

        st.write("Ты юрист, который хорошо разбирается в текстах законов.")
        system_message_2 = st.text_input(
            "Введите системное сообщение для экспертного анализа:"
        )
        st.write("""
    Напиши экспертно-правовой комментарий об изменениях в статье закона, основываясь на выдержках из научной работы.
    Изменения в законе: {query}
    Выдержки из научной работы: {expertise}
    В ответе делай отсылку к научной работе. Ответ юридическим языком:""")
        instruction_2 = st.text_input("Введите инструкцию для экспертного анализа:")

    process_button = st.button("Обработать данные")

    if process_button and law_old is not None and law_actual is not None:
        law_old = law_old.read().decode("cp1251")
        law_actual = law_actual.read().decode("cp1251")

        df = splitting_wrapped(law_old, law_actual)

        result = []
        with st.spinner("Анализ различий..."):
            for _, row in df.iterrows():
                article_old = row["Старая редакция"]
                article_new = row["Новая редакция"]
                result.append(
                    compare_summarize(
                        article_old, article_new, system_message_1, instruction_1
                    )
                )
            st.success("Завершено!")
        if debug_mode:
            st.write(result)

        final_answer = ""
        with st.spinner("Подготовка экспертного мнения..."):
            for query in result:
                expertise = faiss_db.similarity_search_with_score(query, k=5)
                answer = generate_analysis(
                    query, expertise, system_message_2, instruction_2
                )
                final_answer += answer + "\n\n"
            st.success("Завершено!")

        st.write(final_answer)


if __name__ == "__main__":
    main()
