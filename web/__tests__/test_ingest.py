from ..ingest import get_topmost_heading, get_doc_heading, get_file_name, split_docs, add_metadata_to_docs
from .helper import create_doc


def test_get_topmost_heading_empty():
    document = create_doc()
    heading = get_topmost_heading(document)
    assert heading is None


def test_get_topmost_heading():
    document = create_doc("# heading")
    heading = get_topmost_heading(document)
    assert heading == 'heading'

    document = create_doc("#heading")
    heading = get_topmost_heading(document)
    assert heading == 'heading'


def test_get_doc_heading():
    document = create_doc("# heading")
    heading = get_doc_heading(document)
    assert heading == 'heading'

    document = create_doc("no heading", {'source': 'my/file-with-long-name.md'})
    heading = get_doc_heading(document)
    # @T00D00 - uppercase
    assert heading == 'file with long name'

    # @T00D00 - frontmatter fallback


def test_get_file_name():
    document = create_doc("", {'source': 'my/file.md'})
    filename = get_file_name(document)
    assert filename == 'my/file.md'

    # @T00D00 - empty key


def test_split_docs_empty():
    document = create_doc("", {'source': 'my/file.md'})
    split = split_docs([document])
    assert len(split) == 0


def test_split_docs_single():
    document = create_doc("x" * 3000, {'source': 'my/file.md'})
    split = split_docs([document])
    assert len(split) == 1


# @T00D00
# def test_split_docs_two():
#    document = create_doc("x" * 3001, {'source': 'my/file.md'})
#    split = split_docs([document])
#    assert len(split) == 2

def test_add_metadata_to_docs():
    docs = [
        create_doc("", {'source': 'some/source.md'}),
        create_doc("# some heading", {'source': 'another/source.md'}),
    ]

    # @T00D00
    return
    assert docs[0].metadata["heading"] is None
    assert docs[1].metadata["heading"] == "some heading"

    assert docs[0].metadata["id"] == 'some/source'
    assert docs[1].metadata["id"] == "another/source"
