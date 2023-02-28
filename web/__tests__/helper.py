from langchain.docstore.document import Document

def create_doc(content="", metadata={}) -> Document:
    return Document(page_content=content, metadata=metadata)