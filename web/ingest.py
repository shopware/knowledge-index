from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

from filecmp import dircmp
import os
import shutil
import json
import hashlib

from .config import get_embedding_fn
from .config import data_dir, db_dir


def get_topmost_heading(doc):
    for line in doc.page_content.splitlines():
        line = line.strip()
        if line.startswith("#"):
            return line
    return None


def get_file_name(doc):
    return doc.metadata["source"]


def ingest():
    current_dir = data_dir()
    ingested_dir = current_dir + "_ingested"

    loader = DirectoryLoader(current_dir, glob="**/*.md", loader_cls=TextLoader)

    docs = loader.load()

    # Remove documents that are too short
    docs = [doc for doc in docs if len(doc.page_content) > 500]

    for doc in docs:
        heading = get_topmost_heading(doc).lstrip("# ")
        if heading is None:
            heading = get_file_name().split("/")[-1].rstrip(".md").replace("-", " ")
        print(heading)
        doc.metadata["heading"] = heading

    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=3000, chunk_overlap=0
    )
    docs_splitted = text_splitter.split_documents(docs)

    print(f"Loaded {len(docs)} documents.")
    print(f"Splitted into {len(docs_splitted)} chunks.")

    db = FAISS.from_documents(docs_splitted, get_embedding_fn())

    FAISS.save_local(db, db_dir())

    # mark as ingested
    if os.path.isdir(ingested_dir):
        shutil.rmtree(ingested_dir)
    shutil.copytree(current_dir, ingested_dir)

    return True


def ingest_diff():
    current_dir = data_dir()
    ingested_dir = current_dir + "_ingested"

    if not os.path.isdir(current_dir):
        print(f"Nothing to ingest.")
        # nothing to ingest
        return False

    if not os.path.isdir(ingested_dir):
        print(f"Full ingestion.")
        # not ingested yet, full ingestion
        return ingest()

    comparison = dircmp(ingested_dir, current_dir)
    print(f"Comparing directories.")

    diff = get_diff_files(comparison, {"deleted": [], "added": [], "updated": []})

    json_formatted_str = json.dumps(diff, indent=2)
    print(json_formatted_str)

    return False # TBD


def get_diff_files(dcmp, diff):
    # collect updated files
    for name in dcmp.diff_files:
        fullname = os.path.join(dcmp.left, name)
        diff['updated'].append({
            'name': fullname,
            'old': hashlib.md5(open(fullname, 'rb').read()).hexdigest(),
            'new': hashlib.md5(open(os.path.join(dcmp.right, name), 'rb').read()).hexdigest()
        })

    # collect deleted files
    for name in dcmp.left_only:
        fullname = os.path.join(dcmp.left, name)
        diff['deleted'].append({
            'name': fullname,
            'old': hashlib.md5(open(fullname, 'rb').read()).hexdigest(),
            'new': None
        })

    # collect added files
    for name in dcmp.right_only:
        fullname = os.path.join(dcmp.right, name)  # read from new dir
        diff['added'].append({
            'name': fullname,
            'old': None,
            'new': hashlib.md5(open(fullname, 'rb').read()).hexdigest()
        })

    # get diff from sub dirs
    for sub_dcmp in dcmp.subdirs.values():
        diff = get_diff_files(sub_dcmp, diff)

    return diff
