from langchain.vectorstores.chroma import Chroma
from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate
from embedding import getEmbeddings  
from langchain_core.prompts import ChatPromptTemplate

PROMPT_TEMPLATE =  """Use the following pieces of context given inside ``` to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
        {context}
        Question: {question}
        Helpful Answer:"""

def getAnswer(query_text):
    embedding = getEmbeddings()  
    db = Chroma(persist_directory='chroma', embedding_function=embedding)
    results = db.similarity_search_with_score(query_text, k=3)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    
    model = Ollama(model="phi3")
    response_text = model.invoke(prompt)
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(response_text)
    return response_text


