from langchain.vectorstores import FAISS

from .config import get_embedding_fn


def query(query: str):
    embeddings = OpenAIEmbeddings()

    db = FAISS.load_local("_db", get_embedding_fn())

    results = db.similarity_search_with_score(query, 5)

    return results
