import streamlit as st
from src.FAISS import faiss_db
from src.comparison import splitting_wrapped
from src.gigachat import compare_summarize, generate_analysis


def main():
    st.title("Загрузка текстовых файлов")

    law_old = st.file_uploader("Загрузите старую редакцию", type=["txt"])
    law_actual = st.file_uploader("Загрузите новую редакцию", type=["txt"])

    if law_old is not None and law_actual is not None:
        law_old = law_old.read().decode("cp1251")
        law_actual = law_actual.read().decode("cp1251")

        df = splitting_wrapped(law_old, law_actual)

        result = []
        with st.spinner('Анализ различий...'):
            for _, row in df.iterrows():
                article_old = row['Старая редакция']
                article_new = row['Новая редакция']
                result.append(compare_summarize(article_old, article_new))
            st.success('Завершено!')


        final_answer = ''
        with st.spinner('Подготовка экспертного мнения...'):
            for query in result:
                expertise = faiss_db.similarity_search_with_score(query, k=5)
                answer = generate_analysis(query,expertise)
                final_answer += answer + '\n\n'
            st.success('Завершено!')

        st.write(final_answer)


    

if __name__ == "__main__":
    main()
