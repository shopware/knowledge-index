from web.config import get_embedding_fn, db_dir
from web.vector_store import FaissMap

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQAWithSourcesChain, RetrievalQA, LLMChain, ConversationalRetrievalChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT
from langchain.schema.runnable import RunnablePassthrough
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.callbacks import get_openai_callback
from langchain.cache import SQLiteCache
from langchain.globals import set_llm_cache
from langchain import hub

from .tracking import send_ga4_event, send_event

async def generate_answer(question: str, collection=None):

    #event_category = 'ExampleCategory'
    #event_action = 'ExampleAction'
    #await send_ga4_event(event_category, event_action)

    #return {"response": "Sent to GA"}
    #

    # https://python.langchain.com/docs/use_cases/question_answering/vector_db_qa
    model_name = "gpt-3.5-turbo"
    # model_name = "gpt-4"

    search_index = FaissMap.load_local(db_dir(collection), get_embedding_fn())
    llm = OpenAI(
        temperature=0.0,
        max_tokens=512,
        #model_name=model_name,
        batch_size=5
    )
    
    factory = AnsweringFactory()
    output = None

    # https://python.langchain.com/docs/modules/model_io/llms/token_usage_tracking
    cb = get_openai_callback()

    # https://python.langchain.com/docs/integrations/llms/llm_caching
    set_llm_cache(SQLiteCache(database_path=".langchain.db"))

    with get_openai_callback() as cb:
        if True:
            mode = 'chatbot'
            instance = factory.create(mode, search_index, llm)

            output = instance.reformat(instance.run(question))
        else:
            results = {}
            for mode in factory.getMapper():
                instance = factory.create(mode, search_index, llm)

                results[mode] = instance.reformat(instance.run(question))

            output = results

        # track event
        await send_event('all', 'qa', {**{"question": question}, **cb.__dict__})

        output['stats'] = cb
    
    return output


class AnsweringInterface:
    def __init__(self, search_index, llm):
        self.search_index = search_index
        self.llm = llm

    def run(self, question: str):
        pass

    def meta(self):
        pass

    def getRetriever(self):
        return self.search_index.as_retriever()
    
    def getDocuments(self, question: str):
        return self.getRetriever().get_relevant_documents(question)

    def splitAnswerAndSources(self, answer):
        split = answer.split('\nSOURCES: ')

        return {
            'answer': split[0],
            'sources': split[1],
        }

    def reformat(self, output):
        if 'sources' not in output:
            output['sources'] = []
        elif output['sources'] == 'None.':
            output['sources'] = []
        else:
            output['sources'] = output['sources'].split(', ')

        return output


class AnsweringFactory:
    def getMapper(self):
        return {
            'noprompt': NoPrompt,
            'stuffedprompt': StuffedPrompt,
            'ragchain': RagChain,
            'mapreduce': MapReduce,
            'italian': Italian,
            'reducedprompt': ReducedPrompt,
            # 'testchat': TestChat,
            'anothertestchat': AnotherTestChat,
            'chatbot': Chatbot,
        }

    def create(self, name: str, search_index, llm) -> AnsweringInterface:
        mapping = self.getMapper()

        selected_class = mapping.get(name)

        if selected_class:
            return selected_class(search_index, llm)
        
        raise ValueError("Incorrect answering implementation. Available: " + ','.join(mapping.keys()))


class NoPrompt(AnsweringInterface):
    def run(self, question: str):
        chain = RetrievalQAWithSourcesChain.from_chain_type(
            self.llm,
            chain_type="map_reduce",
            retriever=self.getRetriever(),
        )

        return chain({"question": question}, return_only_outputs=True)
    
    def meta(self):
        return {
            "prompt": None,
            "chain": "RetrievalQAWithSourcesChain",
            "type": "map_reduce",
        }

class StuffedPrompt(AnsweringInterface):
    def run(self, question: str):
        prompt_template = """Use the context below to provide a detailed answer for the question below.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Transform the answer to the markdown format.

        {context}
        
        Question: {question}
        Answer:"""

        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        # chain = LLMChain(llm=llm, prompt=PROMPT)
        chain = RetrievalQA.from_chain_type(
            self.llm,
            chain_type="stuff",
            retriever=self.getRetriever(),
            chain_type_kwargs = {"prompt": PROMPT}
        )

        result = chain(question, return_only_outputs=True);

        return {
            'answer': result['result'],
        }


class RagChain(AnsweringInterface):
    def run(self, question: str):
        # https://python.langchain.com/docs/use_cases/question_answering/
        template = """Use the following pieces of context to answer the question at the end. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer. 
        Use three sentences maximum and keep the answer as concise as possible.
        Transform code to markdown.
        {context}
        Question: {question}
        Helpful Answer:"""
        rag_prompt_custom = PromptTemplate.from_template(template)

        rag_chain = (
            {"context": self.getRetriever(), "question": RunnablePassthrough()} | rag_prompt_custom | self.llm
        )

        return {
            'answer': rag_chain.invoke(question),
        }

class MapReduce(AnsweringInterface):
    def run(self, question: str):
        # https://python.langchain.com/docs/use_cases/question_answering/in_memory_question_answering
        chain = load_qa_chain(self.llm, chain_type="map_reduce")
        docs = self.getDocuments(question)
        
        result = chain({"input_documents": docs, "question": question}, return_only_outputs=True)

        return {
            'answer': result['output_text'],
        }

class Italian(AnsweringInterface):
    def run(self, question: str):
        question_prompt_template = """Use the following portion of a long document to see if any of the text is relevant to answer the question.
        Return any relevant text translated into italian.
        {context}
        Question: {question}
        Relevant text, if any, in Italian:"""
        QUESTION_PROMPT = PromptTemplate(
            template=question_prompt_template, input_variables=["context", "question"]
        )

        combine_prompt_template = """Given the following extracted parts of a long document and a question, create a final answer italian.
        If you don't know the answer, just say that you don't know. Don't try to make up an answer.

        QUESTION: {question}
        =========
        {summaries}
        =========
        Answer in Italian:"""
        COMBINE_PROMPT = PromptTemplate(
            template=combine_prompt_template, input_variables=["summaries", "question"]
        )
        chain = load_qa_chain(self.llm, chain_type="map_reduce", return_map_steps=True, question_prompt=QUESTION_PROMPT, combine_prompt=COMBINE_PROMPT)
        docs = self.getDocuments(question)

        result = chain({"input_documents": docs, "question": question}, return_only_outputs=True)

        return {
            'answer': result['output_text'],
        }

class ReducedPrompt(AnsweringInterface):
    def run(self, question: str):
        question_prompt_template = """Use the following portion of a long document to see if any of the text is relevant to answer the question.
        Return any relevant text.
        {context}
        Question: {question}
        Relevant text:"""
        QUESTION_PROMPT = PromptTemplate(
            template=question_prompt_template, input_variables=["context", "question"]
        )

        combine_prompt_template = """Given the following extracted parts of a long document and a question, create a final answer.
        If you don't know the answer, just say that you don't know. Don't try to make up an answer.

        QUESTION: {question}
        =========
        {summaries}
        =========
        Answer:"""
        COMBINE_PROMPT = PromptTemplate(
            template=combine_prompt_template, input_variables=["summaries", "question"]
        )
        chain = load_qa_chain(self.llm, chain_type="map_reduce", return_map_steps=True, question_prompt=QUESTION_PROMPT, combine_prompt=COMBINE_PROMPT)
        docs = self.getDocuments(question)

        result = chain({"input_documents": docs, "question": question}, return_only_outputs=True)

        return {
            'answer': result['output_text'],
        }

class TestChat(AnsweringInterface):
    def run(self, question: str):
        # NOT WORKING, extra fields not permitted
        # https://github.com/langchain-ai/langchain/issues/5096
        combine_template = "Write a summary of the following text:\n\n{summaries}"
        combine_prompt_template = PromptTemplate.from_template(template=combine_template)

        question_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer. 
        {context}
        Question: {question}
        Helpful Answer:"""
        question_prompt_template = PromptTemplate.from_template(template=question_template)

        # create retriever chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            # mmr > for diversity in documents
            # Set fetch_k value to get the fetch_k most similar search. This is basically semantic search
            retriever=self.getRetriever(),
            return_source_documents=True,
            chain_type="map_reduce",
            #chain_type_kwargs={"question_prompt": question_prompt_template, "combine_prompt": combine_prompt_template}
            chain_type_kwargs={"prompt": combine_prompt_template}
        )

        # call QA chain
        return qa_chain({"query": question})

class AnotherTestChat(AnsweringInterface):
    def run(self, question: str):
        qa_chain = load_qa_chain(self.llm, chain_type="stuff")
        qa = RetrievalQA(combine_documents_chain=qa_chain, retriever=self.getRetriever())

        return {
            'answer': qa.run(question),
        }

class Chatbot(AnsweringInterface):
    def run(self, question: str):
        #chatbot = ConversationalRetrievalChain.from_llm(
        #            llm=llm, 
        #           condense_question_llm=ChatOpenAI(temperature=0, model='gpt-3.5-turbo'),
        #            retriever=retriever,
        #            chain_type="map_reduce",
        #            memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True), 
        #           verbose=True,
        #            #return_generated_question=<BOOL>,
        #            #get_chat_history=lambda h : h, 
        #            return_source_documents=True
        #)

        question_generator = LLMChain(llm=self.llm, prompt=CONDENSE_QUESTION_PROMPT)
        #doc_chain = load_qa_chain(llm, chain_type="map_reduce")
        doc_chain = load_qa_with_sources_chain(self.llm, chain_type="map_reduce")

        chatbot = ConversationalRetrievalChain(
            retriever=self.getRetriever(),
            question_generator=question_generator,
            combine_docs_chain=doc_chain,
        )

        chat_history = []
        result = chatbot({"question": question, "chat_history": chat_history})

        return self.splitAnswerAndSources(result['answer'])