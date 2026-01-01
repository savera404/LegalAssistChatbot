#you need to run this code only once

from langchain_community.document_loaders import PyPDFLoader,DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS



#load pdf
DATA_PATH=r"D:\LegalAssist_chatbot\data"
def load_pdfs(data):
    loader=DirectoryLoader(data, glob='*.pdf',loader_cls=PyPDFLoader)
    documents=loader.load()
    return documents

document=load_pdfs(data=DATA_PATH)
# print("number of pages: ", len(document))

#create chunks
def create_chunks(extracted_data):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
    text_chunks=text_splitter.split_documents(extracted_data)
    return text_chunks
text_chunks=create_chunks(extracted_data=document)
#print("number of chunks: ", len(text_chunks))

#create embeddings
def embedding_model():
    embedding_model=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embedding_model

embedding_model=embedding_model()

#create faiss vectorstore
DB_FAISS_PATH='vectorstore/faiss_store'
db=FAISS.from_documents(text_chunks,embedding_model)
db.save_local(DB_FAISS_PATH)