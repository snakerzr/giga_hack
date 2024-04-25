from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from src.FAISS import faiss_db
from src.comparison import splitting_wrapped
from src.gigachat import compare_summarize, generate_analysis

app = FastAPI()

class LawTexts(BaseModel):
    law_old: str
    law_actual: str
    system_message_1: str | None
    instruction_1: str | None
    system_message_2: str | None
    instruction_2: str | None

@app.post("/analyze_laws/")
async def analyze_laws(law_texts: LawTexts):
    try:
        df = splitting_wrapped(law_texts.law_old, law_texts.law_actual)
        
        result = []
        for _, row in df.iterrows():
            article_old = row['Старая редакция']
            article_new = row['Новая редакция']
            summarized = compare_summarize(article_old, article_new, law_texts.system_message_1, law_texts.instruction_1)
            result.append(summarized)
        
        final_answer = ''
        for query in result:
            expertise = faiss_db.similarity_search_with_score(query, k=5)
            answer = generate_analysis(query, expertise, law_texts.system_message_2, law_texts.instruction_2)
            final_answer += answer + '\n\n'

        return {"result": final_answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

