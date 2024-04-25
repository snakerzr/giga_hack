import pandas as pd
import re
import difflib

def splitting_wrapped(old_version, new_version):
        
    # Разделение текста на статьи, разделы, подразделы, главы
    def split_text_into_fragments_with_headers(text):
        # create pattern, find matches
        pattern = r'(Статья\s+\d+\.|Раздел\s+\d+\.|Подраздел\s+\d+\.|Глава\s+\d+\.)\s*(.+?)(?=(Статья\s+\d+\.|Раздел\s+\d+\.|Подраздел\s+\d+\.|Глава\s+\d+\.)|$)'
        fragments = re.findall(pattern, text, re.DOTALL)

        result = []
        for fragment in fragments:
            full_fragment = fragment[0].strip() + ' ' + fragment[1].strip()
            result.append(full_fragment.strip())

        return result
    
    # Создание DataFrame с разбивкой по статьям, с указанием номера статьи
    def collect_heads_pd(articles):
        head_articles = []

        for t in articles:
            head = re.search(r'(Статья\s+\d+\.(\s+\d+\.)?)', t).group()
            head_articles.append(head)

        df = pd.DataFrame(articles, \
                 head_articles).reset_index().rename(columns={'index': 'Номер статьи', 0: 'Текст статьи'})
        return df
        
    # Разбивка текста, удаление заголовков
    articles_old = split_text_into_fragments_with_headers(old_version)[2:]
    articles_new = split_text_into_fragments_with_headers(new_version)[2:]   
    
    # Создание двух DataFrame, содержащих статьи старой и новой редакции закона
    df_old = collect_heads_pd(articles_old).rename(columns={'Текст статьи': 'Старая редакция'})
    df_new = collect_heads_pd(articles_new).rename(columns={'Текст статьи': 'Новая редакция'})
    
    # Объединение, заполнение пропусков
    df_merged = df_new.merge(df_old, how='outer').fillna('none')
    
    # Сравнение текстов двух разных редакций закона, подсчет степени сходства текстов (в отдельной колонке)
    df_merged['Степень сходства'] = df_merged['Номер статьи']
    for i in range(len(df_merged)):
        df_merged['Степень сходства'].iloc[i] = difflib.SequenceMatcher(None, df_merged['Новая редакция'].iloc[i].split(), \
                            df_merged['Старая редакция'].iloc[i].split()).ratio()
        
    return df_merged