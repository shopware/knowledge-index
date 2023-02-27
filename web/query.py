from langchain.vectorstores import FAISS

from .config import get_embedding_fn, db_dir
from .vector_store import FaissMap


def query(query: str, collection):
    db = FaissMap.load_local(db_dir(collection), get_embedding_fn())

    results = db.similarity_search_with_score(query, 5)

    return results


def query_by_id(id: str, collection):
    db = FaissMap.load_local(db_dir(collection), get_embedding_fn())

    results = db.similarity_search_by_id(id, 5)

    return results
