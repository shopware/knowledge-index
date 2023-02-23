from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

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
    loader = DirectoryLoader(data_dir(), glob="**/*.md", loader_cls=TextLoader)

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

    return True
