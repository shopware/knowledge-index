from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document

from filecmp import dircmp
import os
import shutil
import json
import hashlib

from .config import get_embedding_fn
from .config import data_dir, db_dir
from .vector_store import FaissMap


def get_topmost_heading(doc):
    for line in doc.page_content.splitlines():
        line = line.strip()
        if line.startswith("#"):
            return line
    return None


def get_file_name(doc):
    return doc.metadata["source"]

def split_docs(docs):
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=3000, chunk_overlap=0
    )
    docs_splitted = text_splitter.split_documents(docs)

    print(f"Loaded {len(docs)} documents.")
    print(f"Splitted into {len(docs_splitted)} chunks.")

    return docs_splitted

def add_metadata_to_docs(docs, current_dir):
    for doc in docs:
        heading = get_topmost_heading(doc).lstrip("# ")
        if heading is None:
            heading = get_file_name(doc).split("/")[-1].rstrip(".md").replace("-", " ")
        print(heading)
        doc.metadata["heading"] = heading
        doc.metadata["id"] = os.path.relpath(get_file_name(doc), current_dir)


def ingest(collection):
    current_dir = data_dir(collection)
    ingested_dir = current_dir + "_ingested"

    loader = DirectoryLoader(current_dir, glob="**/*.md", loader_cls=TextLoader)

    docs = loader.load()

    # Remove documents that are too short
    docs = [doc for doc in docs if len(doc.page_content) > 500]

    # add heading and id metadata
    add_metadata_to_docs(docs, current_dir)

    # split docs into chunks
    docs_splitted = split_docs(docs)

    # use LangChain VectoreStore from_documents method
    db = FaissMap.from_documents(docs_splitted, get_embedding_fn())

    # create a new index
    FaissMap.save_local(db, db_dir(collection))

    # mark as ingested
    if os.path.isdir(ingested_dir):
        shutil.rmtree(ingested_dir)
    shutil.copytree(current_dir, ingested_dir)

    return True


def get_doc_from_file(file):
    metadata = {
        "source": file["name"],
        "heading": "custom heading",
        "id": file["name"]
    }
    f = open(file["name"], "r")
    content = f.read()
    f.close()
    return Document(page_content=content, metadata=metadata)

def ingest_diff(collection):
    current_dir = data_dir(collection)
    ingested_dir = current_dir + "_ingested"

    if not os.path.isdir(current_dir):
        print(f"Nothing to ingest.")
        # nothing to ingest
        return False

    if not os.path.isdir(ingested_dir):
        print(f"Full ingestion.")
        # not ingested yet, full ingestion
        return ingest(collection)

    comparison = dircmp(ingested_dir, current_dir)
    print(f"Comparing directories.")

    diff = get_diff_files(comparison, {"deleted": [], "added": [], "updated": []})

    # tmp debug
    json_formatted_str = json.dumps(diff, indent=2)
    print(json_formatted_str)

    # 1 - create a new index for updated and new files
    docs = []
    for file in diff["added"]:
        docs.append(get_doc_from_file(file))
    for file in diff["updated"]:
        docs.append(get_doc_from_file(file))

    # split docs
    docs_splitted = split_docs(docs)

    # create a partial db
    db = FaissMap.from_documents(docs_splitted, get_embedding_fn())

    # merge indexes
    print(db)

    # 2 - remove deleted files

    return False  # TBD


def get_diff_files(dcmp, diff):
    # collect updated files
    for name in dcmp.diff_files:
        fullname = os.path.join(dcmp.left, name)
        diff["updated"].append(
            {
                "name": fullname,
                "old": hashlib.md5(open(fullname, "rb").read()).hexdigest(),
                "new": hashlib.md5(
                    open(os.path.join(dcmp.right, name), "rb").read()
                ).hexdigest(),
            }
        )

    # collect deleted files
    for name in dcmp.left_only:
        fullname = os.path.join(dcmp.left, name)
        diff["deleted"].append(
            {
                "name": fullname,
                "old": hashlib.md5(open(fullname, "rb").read()).hexdigest(),
                "new": None,
            }
        )

    # collect added files
    for name in dcmp.right_only:
        fullname = os.path.join(dcmp.right, name)  # read from new dir
        diff["added"].append(
            {
                "name": fullname,
                "old": None,
                "new": hashlib.md5(open(fullname, "rb").read()).hexdigest(),
            }
        )

    # get diff from sub dirs
    for sub_dcmp in dcmp.subdirs.values():
        diff = get_diff_files(sub_dcmp, diff)

    return diff
