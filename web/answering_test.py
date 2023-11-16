

if mode == 'third':
    # NOT WORKING
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
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs = {"prompt": PROMPT}
    )

    return chain(question, return_only_outputs=True)
    return chain.run(question)
elif mode == 'fifth':
    # NOT WORKING, see sixth
    # https://python.langchain.com/docs/use_cases/question_answering/in_memory_question_answering
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
    chain = load_qa_chain(llm, chain_type="map_reduce", return_map_steps=True, question_prompt=QUESTION_PROMPT, combine_prompt=COMBINE_PROMPT)
    docs = retriever.get_relevant_documents(question)
    
    return chain({"input_documents": docs, "question": question}, return_only_outputs=True)
elif mode == 'sixth':
    # NOT WORKING
    # https://python.langchain.com/docs/use_cases/question_answering/in_memory_question_answering
    template = """Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer. 
    Use three sentences maximum and keep the answer as concise as possible.
    Transform code to markdown.
    {context}
    Question: {question}
    Helpful Answer:"""
    QUESTION_PROMPT = PromptTemplate(
        template=template, input_variables=["context", "question"]
    )
    chain = load_qa_chain(llm, chain_type="map_reduce", prompt=QUESTION_PROMPT)
    docs = retriever.get_relevant_documents(question)
    
    return chain({"input_documents": docs, "question": question}, return_only_outputs=True)