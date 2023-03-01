from typing import List
from ..query import map_result
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
