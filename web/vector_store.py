import faiss
import pickle
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

import numpy as np

from langchain.vectorstores.base import VectorStore
from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings


class FaissMap(VectorStore):
    def __init__(
        self,
        embedding_function: Callable,
        index: Any,
        docstore: Dict[str, Document],
        index_to_docstore_id: Dict[int, str],
    ):
        self.source_mapping = {}
        self.embedding_function = embedding_function
        self.index = index
        self.docstore = docstore
        self.index_to_docstore_id = index_to_docstore_id

    def add_texts(
        self,
        texts: Iterable[str],
        metadatas: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> List[str]:
        return []

    def similarity_search_with_score_by_vector(
        self, embedding: List[float], k: int = 4
    ) -> List[Tuple[Document, float]]:
        scores, indices = self.index.search(np.array([embedding], dtype=np.float32), k)
        docs = []
        for j, i in enumerate(indices[0]):
            if i == -1:
                # This happens when not enough docs are returned.
                continue
            _id = self.index_to_docstore_id[i]
            doc = self.docstore.get(_id)
            if not isinstance(doc, Document):
                raise ValueError(f"Could not find document for id {_id}, got {doc}")
            docs.append((doc, scores[0][j]))
        return docs

    def similarity_search_with_score(
        self, query: str, k: int = 4
    ) -> List[Tuple[Document, float]]:
        embedding = self.embedding_function(query)
        docs = self.similarity_search_with_score_by_vector(embedding, k)
        return docs

    def similarity_search_by_vector(
        self, embedding: List[float], k: int = 4, **kwargs: Any
    ) -> List[Document]:
        docs_and_scores = self.similarity_search_with_score_by_vector(embedding, k)
        return [doc for doc, _ in docs_and_scores]

    def similarity_search(
        self, query: str, k: int = 4, **kwargs: Any
    ) -> List[Document]:
        docs_and_scores = self.similarity_search_with_score(query, k)
        return [doc for doc, _ in docs_and_scores]

    def similarity_search_by_id(self, id: str, k: int = 4) -> List[Document]:
        index_id = self.docstore[id].metadata["index_id"]
        embedding = self.index.reconstruct(index_id)
        return self.similarity_search_with_score_by_vector(embedding, k)

    @classmethod
    def from_texts(
        cls,
        texts: List[str],
        embedding: Embeddings,
        metadatas: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> Any:
        embeddings = embedding.embed_documents(texts)
        index = faiss.IndexFlatL2(len(embeddings[0]))
        index.add(np.array(embeddings, dtype=np.float32))
        documents = []
        assert len(texts) == len(metadatas)
        for i, text in enumerate(texts):
            metadata = metadatas[i] if metadatas else {}
            metadata["index_id"] = i
            documents.append(Document(page_content=text, metadata=metadata))

        docstore = {doc.metadata["source"]: doc for doc in documents}

        index_to_id = {i: doc.metadata["source"] for i, doc in enumerate(documents)}
        return cls(embedding.embed_query, index, docstore, index_to_id)

    def save_local(self, folder_path: str) -> None:
        path = Path(folder_path)
        path.mkdir(exist_ok=True, parents=True)

        # save index separately since it is not picklable
        faiss.write_index(self.index, str(path / "index.faiss"))

        # save docstore and index_to_docstore_id
        with open(path / "index.pkl", "wb") as f:
            pickle.dump((self.docstore, self.index_to_docstore_id), f)

    @classmethod
    def load_local(cls, folder_path: str, embeddings: Embeddings) -> Any:
        path = Path(folder_path)
        # load index separately since it is not picklable
        index = faiss.read_index(str(path / "index.faiss"))

        # load docstore and index_to_docstore_id
        with open(path / "index.pkl", "rb") as f:
            docstore, index_to_docstore_id = pickle.load(f)
        return cls(embeddings.embed_query, index, docstore, index_to_docstore_id)
