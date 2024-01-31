from typing import Dict

from .config import get_embedding_fn, db_dir
from .vector_store import FaissMap


def query(query: str, collection, num: int = 5):
    db = FaissMap.load_local(db_dir(collection), get_embedding_fn())

    results = db.similarity_search_with_score(query, num)

    return results


def query_by_id(id: str, collection, num: int = 5):
    db = FaissMap.load_local(db_dir(collection), get_embedding_fn())

    results = db.similarity_search_by_id(id, num)

    return results



def query_n_with_fallback(id: str, collection, num: int = 5, limit: int = 5, depth: int = 3, filters: Dict = {}):
    try:
        results = query_by_id(id, collection, limit)
    except KeyError:
        results = query(id, collection, limit)

    # filter out current document
    results = [result for result in results if result[0].metadata["id"] != id]

    # filter out inclusions and exclusions
    results = apply_filter(results, filters)

    # try to fetch more, recursively
    count = count_unique_pre_results(results)
    if count < num and depth > 0:
        print("Required " + str(num) + " got " + str(count) + " unique")
        return query_n_with_fallback(id, collection, num, limit + num, depth - 1, filters)

    return results


def apply_filter(results, filters):
    # empty filter
    if "include" not in filters and "exclude" not in filters:
        return results

    inter_results = []
    for result in results:
        is_excluded = False

        # 1 - mark as excluded
        if "exclude" in filters:
            for filter in filters["exclude"]:
                if result[0].metadata["id"].startswith(filter):
                    is_excluded = True
                    break

        # 2 - check for manual inclusion
        if is_excluded and "include" in filters:
            for filter in filters["include"]:
                if result[0].metadata["id"].startswith(filter):
                    is_excluded = False
                    break

        # 3 - keep when not excluded (by default, or when re-included)
        if not is_excluded:
            inter_results.append(result)

    return inter_results

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


def count_unique_pre_results(results, key: str = "id"):
    seen = set()
    for result in results:
        if result[0].metadata[key] not in seen:
            seen.add(result[0].metadata[key])

    return len(seen)

def unique_results(results, key: str = "id"):
    unique = []
    seen = set()
    for result in results:
        if result[key] in seen:
            continue

        unique.append(result)
        seen.add(result[key])

    return unique
