import os

from langchain_community.embeddings import TensorflowHubEmbeddings
from langchain_openai import (
    AzureChatOpenAI,
    AzureOpenAIEmbeddings,
    ChatOpenAI,
    OpenAIEmbeddings,
)

from .model_config import (
    CHAT_MODEL,
    CHAT_REASONING_EFFORT,
    CHAT_TEMPERATURE,
    EMBEDDING_MODEL,
    ModelConfigurationError,
    get_azure_openai_config,
)


AZURE_COLLECTION = "shopware--operations-portal--test"


def _create_azure_llm(model: str):
    config = get_azure_openai_config()
    if model != config.model:
        raise ModelConfigurationError(
            f"Azure OpenAI deployment is configured for {config.model!r}, got {model!r}"
        )

    return AzureChatOpenAI(
        api_key=config.api_key,
        azure_endpoint=config.endpoint,
        api_version=config.api_version,
        azure_deployment=config.deployment,
        model=config.model,
        temperature=CHAT_TEMPERATURE,
        reasoning_effort=CHAT_REASONING_EFFORT,
    )


def _create_azure_embeddings():
    config = get_azure_openai_config()
    return AzureOpenAIEmbeddings(
        api_key=config.api_key,
        azure_endpoint=config.endpoint,
        api_version=config.api_version,
        azure_deployment=config.embeddings_deployment,
        model=EMBEDDING_MODEL,
    )


class LLMFactory:
    @staticmethod
    def createLLM(model_name: str, collection: str):
        collections = collections_config()

        if collection not in collections:
            collection = "default"

        return collections[collection]["llm"](model_name)

    @staticmethod
    def createEmbeddingFn(collection: str):
        if collection != AZURE_COLLECTION and "OPENAI_API_KEY" not in os.environ:
            collection = "tensorflow"

        collections = collections_config()

        if collection not in collections:
            collection = "default"

        return collections[collection]["embeddings"]()


def collections_config():
    return {
        AZURE_COLLECTION: {
            "llm": _create_azure_llm,
            "embeddings": _create_azure_embeddings,
        },
        "tensorflow": {
            "llm": lambda model: None,
            "embeddings": lambda: TensorflowHubEmbeddings(
                model_url="https://tfhub.dev/google/universal-sentence-encoder-multilingual/3"
            ),
        },
        "default": {
            "llm": lambda model=CHAT_MODEL: ChatOpenAI(
                model=model,
                temperature=CHAT_TEMPERATURE,
                reasoning_effort=CHAT_REASONING_EFFORT,
            ),
            "embeddings": lambda: OpenAIEmbeddings(model=EMBEDDING_MODEL),
        },
    }
