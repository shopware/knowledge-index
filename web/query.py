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


def map_result(result):
    source = result[0].metadata["source"]
    heading = result[0].metadata["heading"]
    excerpt = result[0].page_content
    score = result[1]
    return {"source": source, "score": str(score), "heading": heading}


def map_results(results):
    mappedResults = []

    for result in results:
        mappedResults.append(map_result(result))

    return mappedResults
