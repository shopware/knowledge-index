from langchain.llms import OpenAI, AzureOpenAI

class LLMFactory:
    def create(self, model_name: str):
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
    
    #def createForCollection(self, collection: str, model_name: str):
    #    collections = {
    #        "shopware--operations-portal--test": AzureOpenAI,
    #    }
    #    
    #    return self.create(model_name)