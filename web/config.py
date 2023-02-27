import os
from typing import Union


def get_embedding_fn():
    if "OPENAI_API_KEY" in os.environ:
        from langchain.embeddings.openai import OpenAIEmbeddings

        return OpenAIEmbeddings()
    else:
        from langchain.embeddings import TensorflowHubEmbeddings

        url = "https://tfhub.dev/google/universal-sentence-encoder-multilingual/3"
        return TensorflowHubEmbeddings(model_url=url)

def env_dir(env, dir, collection = Union[None, str]):
    if collection:
        env += "_" + collection.upper()
        dir += "-" + collection

    return {
        "env": env,
        "dir": dir
    }

def data_dir(collection = Union[None, str]):
    conf = env_dir("DATA_DIR", "/data/docs", collection)

    return os.environ.get(conf["env"], conf["dir"])

def db_dir(collection = Union[None, str]):
    conf = env_dir("DB_DIR", "/data/db", collection)

    return os.environ.get(conf["env"], conf["dir"])

def cache_dir():
    conf = env_dir("CACHE_DIR", "/data/cache", None)

    return os.environ.get(conf["env"], conf["dir"])