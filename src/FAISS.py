import os

from dotenv import load_dotenv,find_dotenv

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.gigachat import GigaChatEmbeddings

_ = load_dotenv(find_dotenv())

CREDS = os.environ['CREDS']

FOLDER_PATH_INDEX = "faiss_trained_on_dataset"
NAME_INDEX = "langchains_index"

# количество соседей для кажого ретривера
NEIGHBOUR = 5

embeddings = GigaChatEmbeddings(
    credentials=CREDS, scope='GIGACHAT_API_CORP', verify_ssl_certs=False
)

faiss_db = FAISS.load_local(folder_path=FOLDER_PATH_INDEX, embeddings=embeddings, index_name=NAME_INDEX, allow_dangerous_deserialization=True)
# faiss_db

if __name__ == '__main__':
    query = 'В старой версии закона говорится о возможности обращения взыскания на заложенное имущество по решению суда или во внесудебном порядке. В новой версии уточняется, что обращение взыскания на заложенное имущество осуществляется по решению суда, если стороны не предусмотрели внесудебный порядок.'
    expertise = faiss_db.similarity_search_with_score(query, k=5)
    print(expertise)