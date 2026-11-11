import pytest

from ..model_config import (
    CHAT_MODEL,
    ModelConfigurationError,
    get_azure_openai_config,
)


AZURE_ENV = {
    "AZURE_OPENAI_API_KEY": "azure-key",
    "AZURE_OPENAI_ENDPOINT": "https://example.openai.azure.com",
    "AZURE_OPENAI_DEPLOYMENT": "chat-deployment",
    "AZURE_OPENAI_DEPLOYMENT_EMBEDDINGS": "embedding-deployment",
    "AZURE_OPENAI_MODEL": CHAT_MODEL,
    "AZURE_OPENAI_API_VERSION": "test-api-version",
}


def set_azure_env(monkeypatch, **overrides):
    values = {**AZURE_ENV, **overrides}
    for name, value in values.items():
        if value is None:
            monkeypatch.delenv(name, raising=False)
        else:
            monkeypatch.setenv(name, value)


def test_azure_config_is_explicit(monkeypatch):
    set_azure_env(monkeypatch)

    config = get_azure_openai_config()

    assert config.model == CHAT_MODEL
    assert config.deployment == "chat-deployment"
    assert config.embeddings_deployment == "embedding-deployment"
    assert config.api_version == "test-api-version"


def test_azure_config_rejects_missing_values(monkeypatch):
    set_azure_env(monkeypatch, AZURE_OPENAI_API_VERSION=None)

    with pytest.raises(ModelConfigurationError, match="AZURE_OPENAI_API_VERSION"):
        get_azure_openai_config()


def test_azure_config_rejects_unsupported_model(monkeypatch):
    set_azure_env(monkeypatch, AZURE_OPENAI_MODEL="gpt-4.1-mini")

    with pytest.raises(ModelConfigurationError, match="must be 'gpt-6-luna'"):
        get_azure_openai_config()
