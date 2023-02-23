from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

from .embedding import get_embedding_fn


def ingest():
    loader = DirectoryLoader("data/", glob="**/*.md", loader_cls=TextLoader)

    docs = loader.load()

    # Remove documents that are too short
    docs = [doc for doc in docs if len(doc.page_content) > 500]

    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=3000, chunk_overlap=0
    )
    docs_splitted = text_splitter.split_documents(docs)

    print(f"Loaded {len(docs)} documents.")
    print(f"Splitted into {len(docs_splitted)} chunks.")

    db = FAISS.from_documents(docs_splitted, get_embedding_fn())

    FAISS.save_local(db, "_db")

    return True
