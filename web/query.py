from langchain.vectorstores import FAISS

from .config import get_embedding_fn, db_dir


def query(query: str):
    db = FAISS.load_local(db_dir(), get_embedding_fn())

    results = db.similarity_search_with_score(query, 5)

    return results
