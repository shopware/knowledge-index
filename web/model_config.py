import os
from dataclasses import dataclass


CHAT_MODEL = "gpt-6-luna"
CHAT_MODEL_CONTEXT = 1_050_000
CHAT_REASONING_EFFORT = "none"
CHAT_TEMPERATURE = 0.0
EMBEDDING_MODEL = "text-embedding-ada-002"


class ModelConfigurationError(ValueError):
    """Raised when an LLM provider is configured inconsistently."""


@dataclass(frozen=True)
class AzureOpenAIConfig:
    api_key: str
    endpoint: str
    deployment: str
    embeddings_deployment: str
    model: str
    api_version: str


def get_azure_openai_config() -> AzureOpenAIConfig:
    variables = {
        "AZURE_OPENAI_API_KEY": os.getenv("AZURE_OPENAI_API_KEY"),
        "AZURE_OPENAI_ENDPOINT": os.getenv("AZURE_OPENAI_ENDPOINT"),
        "AZURE_OPENAI_DEPLOYMENT": os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        "AZURE_OPENAI_DEPLOYMENT_EMBEDDINGS": os.getenv(
            "AZURE_OPENAI_DEPLOYMENT_EMBEDDINGS"
        ),
        "AZURE_OPENAI_MODEL": os.getenv("AZURE_OPENAI_MODEL"),
        "AZURE_OPENAI_API_VERSION": os.getenv("AZURE_OPENAI_API_VERSION"),
    }
    missing = [name for name, value in variables.items() if not value]

    if missing:
        raise ModelConfigurationError(
            "Azure OpenAI configuration is incomplete. Missing: "
            + ", ".join(sorted(missing))
        )

    if variables["AZURE_OPENAI_MODEL"] != CHAT_MODEL:
        raise ModelConfigurationError(
            "AZURE_OPENAI_MODEL must be "
            f"{CHAT_MODEL!r}; got {variables['AZURE_OPENAI_MODEL']!r}"
        )

    return AzureOpenAIConfig(
        api_key=variables["AZURE_OPENAI_API_KEY"],
        endpoint=variables["AZURE_OPENAI_ENDPOINT"],
        deployment=variables["AZURE_OPENAI_DEPLOYMENT"],
        embeddings_deployment=variables["AZURE_OPENAI_DEPLOYMENT_EMBEDDINGS"],
        model=variables["AZURE_OPENAI_MODEL"],
        api_version=variables["AZURE_OPENAI_API_VERSION"],
    )
