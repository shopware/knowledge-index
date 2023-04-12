from ..ingest import get_topmost_heading, get_doc_heading, get_doc_description, get_file_name, split_docs, add_metadata_to_docs, get_frontmatter_info
from .helper import create_doc
from datetime import datetime, date
import pytest
import random
import string


def test_get_topmost_heading_empty():
    document = create_doc()
    heading = get_topmost_heading(document)
    assert heading is None


def test_get_topmost_heading():
    document = create_doc("# heading")
    heading = get_topmost_heading(document)
    assert heading == 'heading'

    document = create_doc("#Heading")
    heading = get_topmost_heading(document)
    assert heading == 'Heading'


def test_get_doc_info():
    document = create_doc("""---
title: frontmatter Heading
description: frontmatter Description
---
# heading""")

    heading = get_doc_heading(document)
    description = get_doc_description(document)
    assert heading == 'frontmatter Heading'
    assert description == 'frontmatter Description'

    document = create_doc("# heading")
    heading = get_doc_heading(document)
    description = get_doc_description(document)
    assert heading == 'heading'
    assert description is None

    document = create_doc("no heading", {'source': 'my/file-with-long-name.md'})
    heading = get_doc_heading(document)
    description = get_doc_description(document)
    assert heading == 'File With Long Name'
    assert description is None


def test_get_file_name():
    document = create_doc("", {'source': 'my/file.md'})
    filename = get_file_name(document)
    assert filename == 'my/file.md'


def test_add_metadata_to_docs():
    docs = [
        create_doc("", {'source': 'some/source.md'}),
        create_doc("# some heading", {'source': 'another/source.md'}),
    ]
    add_metadata_to_docs(docs, '')

    assert docs[0].metadata["heading"] == "Source"
    assert docs[1].metadata["heading"] == "some heading"

    assert docs[0].metadata["id"] == 'some/source.md'
    assert docs[1].metadata["id"] == "another/source.md"


def test_correct_datetime_frontmatter():
    content = """---
title: Replace drop-shadow with box-shadow
date: 2022-11-21

---

# Replace drop-shadow with box-shadow
    """

    doc = create_doc(content)

    response = get_frontmatter_info(doc, "date")

    assert isinstance(response, date)


def test_incorrect_datetime_frontmatter():
    content = """---
title: Replace drop-shadow with box-shadow
date: 2022-21-11

---

# Replace drop-shadow with box-shadow
    """

    doc = create_doc(content)

    # catch "soft fail"
    response = get_frontmatter_info(doc, "date")
    assert None == response

    # fails when frontmatter.parse or yaml.load is used
    #with pytest.raises(Exception) as exc_info:
    #    response = get_frontmatter_info(doc, "date")
    # assert str(exc_info.value) == 'month must be in 1..12'
    
    # works (not) with custom frontmatter_parse implementation
    # response = get_frontmatter_info(doc, "date")
    # assert response == "2022-21-11"