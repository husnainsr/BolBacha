import shutil
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain.vectorstores.chroma import Chroma
from embedding import getEmbeddings
import os

DATABASE_PATH='chroma'
DATA_PATH='data'
def loadDocuments(PATH):
    loader = PyPDFDirectoryLoader(DATA_PATH)
    pages = loader.load_and_split()
    return pages
    
def splitDocuments(documents: list[Document]):
    textSplitter=RecursiveCharacterTextSplitter(chunk_size=800,chunk_overlap=80,length_function=len,is_separator_regex=False,)
    return textSplitter.split_documents(documents)


def addToDatabase(chunks:list[Document]):
    db=Chroma(persist_directory=DATABASE_PATH, embedding_function=getEmbeddings())
    chunksIncludingIDs=calculateChunkIDs(chunks)
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")
    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunksIncludingIDs:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
        db.persist()
        result=f"👉 Adding new documents: {len(new_chunks)}"
        return result
    else:
        print("✅ No new documents to add")
        result="✅ No new documents to add"
        return result


def calculateChunkIDs(chunks):
    lastPageID = None
    currentChunkIndex = 0
    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        currentPageID = f"{source}:{page}"
        #If the page ID is the same as the last one, increment the index.
        if currentPageID == lastPageID:
            currentChunkIndex += 1
        else:
            currentChunkIndex = 0
        #Calculate the chunk ID.
        chunk_id = f"{currentPageID}:{currentChunkIndex}"
        lastPageID = currentPageID
        #Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id
    return chunks

def clear_database():
    if os.path.exists(DATABASE_PATH):
        shutil.rmtree(DATABASE_PATH)
        
       


def mainAddData():
    documents= loadDocuments(DATA_PATH)
    chunks=splitDocuments(documents)
    output=addToDatabase(chunks)
    return output
    
