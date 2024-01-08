from langchain.llms import OpenAI, AzureOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.azure_openai import AzureOpenAIEmbeddings

class LLMFactory:
    def createLLM(self, model_name: str, collection: str = None):
        collections = collections_config()
        
        if collection in collections:
            return collections.get(collection)["llm"]()
        
        # https://python.langchain.com/docs/use_cases/question_answering/vector_db_qa
        max_tokens = 1024 # 512
        max_tokens = -1
        #batch_size = 5

        return OpenAI(
            temperature=0.0,
            max_tokens=max_tokens,
            model_name=model_name,
            #batch_size=batch_size
        )
    
    def createEmbeddingFn(self, collection: str = None):
        collections = collections_config()
        
        if collection in collections:
            return collections.get(collection)["embeddings"]()
        
        return OpenAIEmbeddings()
    
    
def collections_config():
    return {
        "shopware--operations-portal--test": {
            "llm": AzureOpenAI,
            "embeddings": AzureOpenAIEmbeddings,
        }
    }