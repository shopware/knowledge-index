from ..ingest import get_topmost_heading, get_doc_heading, get_doc_description, get_file_name, split_docs, add_metadata_to_docs
from .helper import create_doc
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
