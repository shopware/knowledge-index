import os


def get_embedding_fn():
    if "OPENAI_API_KEY" in os.environ:
        from langchain.embeddings.openai import OpenAIEmbeddings

        return OpenAIEmbeddings()
    else:
        from langchain.embeddings import TensorflowHubEmbeddings

        url = "https://tfhub.dev/google/universal-sentence-encoder-multilingual/3"
        return TensorflowHubEmbeddings(model_url=url)


def data_dir():
    return os.environ.get("DATA_DIR", "/data/docs")

def db_dir():
    return os.environ.get("DB_DIR", "/data/db")
