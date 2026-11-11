from unittest.mock import Mock

from .. import llm
from ..answering import ModelFactory
from ..model_config import CHAT_MODEL, CHAT_MODEL_CONTEXT, EMBEDDING_MODEL
from .test_model_config import set_azure_env


def test_direct_openai_uses_supported_chat_model(monkeypatch):
    chat_openai = Mock(return_value=object())
    monkeypatch.setattr(llm, "ChatOpenAI", chat_openai)

    llm.LLMFactory.createLLM(CHAT_MODEL, "default")

    chat_openai.assert_called_once_with(
        model=CHAT_MODEL,
        temperature=0.0,
        reasoning_effort="none",
    )


def test_model_registry_only_contains_luna():
    factory = ModelFactory()

    assert list(factory.getMapper()) == [CHAT_MODEL]
    assert factory.create(CHAT_MODEL).context == CHAT_MODEL_CONTEXT


def test_direct_openai_embeddings_remain_on_ada(monkeypatch):
    embeddings = Mock(return_value=object())
    monkeypatch.setattr(llm, "OpenAIEmbeddings", embeddings)
    monkeypatch.setenv("OPENAI_API_KEY", "openai-key")

    llm.LLMFactory.createEmbeddingFn("default")

    embeddings.assert_called_once_with(model=EMBEDDING_MODEL)


def test_azure_factories_use_validated_configuration(monkeypatch):
    set_azure_env(monkeypatch)
    azure_chat = Mock(return_value=object())
    azure_embeddings = Mock(return_value=object())
    monkeypatch.setattr(llm, "AzureChatOpenAI", azure_chat)
    monkeypatch.setattr(llm, "AzureOpenAIEmbeddings", azure_embeddings)

    llm.LLMFactory.createLLM(CHAT_MODEL, llm.AZURE_COLLECTION)
    llm.LLMFactory.createEmbeddingFn(llm.AZURE_COLLECTION)

    azure_chat.assert_called_once_with(
        api_key="azure-key",
        azure_endpoint="https://example.openai.azure.com",
        api_version="test-api-version",
        azure_deployment="chat-deployment",
        model=CHAT_MODEL,
        temperature=0.0,
        reasoning_effort="none",
    )
    azure_embeddings.assert_called_once_with(
        api_key="azure-key",
        azure_endpoint="https://example.openai.azure.com",
        api_version="test-api-version",
        azure_deployment="embedding-deployment",
        model=EMBEDDING_MODEL,
    )
