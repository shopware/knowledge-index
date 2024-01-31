import os

from langchain.llms import OpenAI, AzureOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.azure_openai import AzureOpenAIEmbeddings
from langchain.embeddings import TensorflowHubEmbeddings

class LLMFactory:
    def createLLM(model_name: str, collection: str = None):
        collections = collections_config()
        
        if collection in collections:
            return collections.get(collection)["llm"](model_name)
        
        # https://python.langchain.com/docs/use_cases/question_answering/vector_db_qa
        return OpenAI(
            temperature=0.0,
            max_tokens=-1, # 1024, 512
            model_name=model_name,
            #batch_size=batch_size
        )
    
    def createEmbeddingFn(collection: str = None):
        if "OPENAI_API_KEY" not in os.environ:
            print("Using Tensorflow")
            return TensorflowHubEmbeddings(model_url="https://tfhub.dev/google/universal-sentence-encoder-multilingual/3")
        
        collections = collections_config()
        
        if collection in collections:
            return collections.get(collection)["embeddings"]()
        
        return OpenAIEmbeddings()
    
    
def collections_config():
    return {
        "shopware--operations-portal--test": {
            "llm": lambda model: AzureOpenAI(
                api_type = "azure",
                api_key = os.getenv("AZURE_OPENAI_API_KEY"),
                azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_version = "2023-05-15",
                
                temperature=0.0,
            ),
            "embeddings": lambda: AzureOpenAIEmbeddings(),
        },
        "tensorflow": {
            "llm": lambda model: None,
            "embeddings": lambda: TensorflowHubEmbeddings(),
        }
    }