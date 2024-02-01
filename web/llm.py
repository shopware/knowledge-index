import os

from langchain.llms import OpenAI, AzureOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.azure_openai import AzureOpenAIEmbeddings
from langchain.embeddings import TensorflowHubEmbeddings

class LLMFactory:
    def createLLM(model_name: str, collection: str = None):
        collections = collections_config()
        
        if collection not in collections:
            collection = 'default'
        
        return collections.get(collection)["llm"](model_name)
    
    def createEmbeddingFn(collection: str = None):
        if "OPENAI_API_KEY" not in os.environ:
            collection = 'tensorflow'
        
        collections = collections_config()
        
        if collection not in collections:
            collection = 'default'
            
        return collections.get(collection)["embeddings"]()
    
    
def collections_config():
    return {
        "shopware--operations-portal--test": {
            "llm": lambda model: AzureOpenAI(
                api_type = "azure",
                api_key = os.getenv("AZURE_OPENAI_API_KEY"),
                azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
                temperature=0.0,
                #api_version = "2023-05-15",
            ),
            "embeddings": lambda: AzureOpenAIEmbeddings(
                openai_api_type = "azure",
                openai_api_key = os.getenv("AZURE_OPENAI_API_KEY"),
                azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_base = os.getenv("AZURE_OPENAI_ENDPOINT"),
                model = "text-embedding-ada-002",
                deployment = "azure-openai-ops-test-ada-002", # azure-openai-opt-test-gpt4
            ),
        },
        "tensorflow": {
            "llm": lambda model: None,
            "embeddings": lambda: TensorflowHubEmbeddings(model_url="https://tfhub.dev/google/universal-sentence-encoder-multilingual/3"),
        },
        # https://python.langchain.com/docs/use_cases/question_answering/vector_db_qa
        "default": {
            "llm": lambda model = "gpt-3.5-turbo": OpenAI(
                temperature=0.0,
                max_tokens=-1,
                model_name=model,
            ),
            "embeddings": lambda: OpenAIEmbeddings(),
        },
    }