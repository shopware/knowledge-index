from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQAWithSourcesChain

from web.config import get_embedding_fn, db_dir
from web.vector_store import FaissMap

from langchain.chains import LLMChain


def generate_answer(question: str, collection=None):
    search_index = FaissMap.load_local(db_dir(collection), get_embedding_fn())

    prompt_template = """Use the context below to provide a detailed answer for the question below.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Transform the answer to the markdown format.
    Context: {context}
    Answer:"""

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context"]
    )

    llm = OpenAI(temperature=0.1, max_tokens=512)

    # chain = LLMChain(llm=llm, prompt=PROMPT)
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm,
        chain_type="map_reduce",
        retriever=search_index.as_retriever(),
        #chain_type_kwargs = {"prompt": PROMPT}
    )

    # docs = search_index.similarity_search(question, k=4)
    # inputs = [{"context": doc.page_content, "question": question} for doc in docs]
    # return chain.apply(inputs)
    return chain({"question": question}, return_only_outputs=True)
