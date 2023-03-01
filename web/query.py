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
    doc = result[0]
    score = result[1]
    id = doc.metadata["id"]
    heading = doc.metadata["heading"]
    description = doc.metadata["description"]

    return {
        "id": id,
        "score": str(score),
        "heading": heading,
        "description": description,
    }


def map_results(results):
    mappedResults = []
    for result in results:
        mappedResults.append(map_result(result))

    return mappedResults


def unique_results(results, key: str = "id"):
    unique = []
    seen = set()
    for result in results:
        if result[key] in seen:
            continue

        unique.append(result)
        seen.add(result[key])

    return unique
