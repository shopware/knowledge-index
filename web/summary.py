from .config import db_dir, get_embedding_fn
from .vector_store import FaissMap

def get_collection_summary(collection: str):
    collection = None

    my_db_dir = db_dir(collection)

    search_index = FaissMap.load_local(my_db_dir, get_embedding_fn())

    # Get all document IDs
    all_doc_ids = list(search_index.index_to_docstore_id.values())

    # Retrieve all documents
    documents = [search_index.docstore[doc_id].metadata for doc_id in all_doc_ids]

    return {
        "documents": documents,
    }