from typing import List
from ..query import map_result, unique_results
from .helper import create_doc


def test_map_results():
    result = [
        create_doc("", {"source": "my/source.md", "heading": "My heading"}),
        0.1
    ]

    mapped_result = map_result(result)

    assert mapped_result["source"] == "my/source.md"
    assert mapped_result["heading"] == "My heading"
    assert mapped_result["score"] == "0.1"


def test_unique_results():
    results = [
        {"source": "a", "score": "0.1"},
        {"source": "a", "score": "0.2"},
        {"source": "b", "score": "0.1"},
        {"source": "c", "score": "0.2"},
    ]

    filtered = unique_results(results)
    keys = []
    for result in filtered:
        keys.append(result["source"])

    assert len(filtered) == 3
    assert keys == ["a", "b", "c"]