from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings

def query(query: str):
    embeddings = OpenAIEmbeddings()

    db = FAISS.load_local('_db', embeddings)

    results = db.similarity_search_with_score(query, 5)

    return results