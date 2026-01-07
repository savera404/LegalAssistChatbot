
# ===============================
# Incremental RAG Ingestion Code
# ===============================

import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# -------------------------------
# PATHS
# -------------------------------
# DATA_PATH = r"D:\LegalAssist_chatbot\data\laws"
DATA_PATH = r"D:\LegalAssist_chatbot\data\case_summaries"
DB_FAISS_PATH = r"D:\LegalAssist_chatbot\vectorstore\faiss_store"
PROCESSED_FILE = r"D:\LegalAssist_chatbot\processed_files.txt"


# -------------------------------
# LOAD EXISTING PROCESSED FILES
# -------------------------------
if os.path.exists(PROCESSED_FILE):
    with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
        processed_files = set(f.read().splitlines())
else:
    processed_files = set()


# # -------------------------------
# # LOAD ONLY NEW PDFs
# # -------------------------------
# def load_new_pdfs(data_path):
#     loader = DirectoryLoader(
#         data_path,
#         glob="**/*.pdf",        # recursive
#         loader_cls=PyPDFLoader
#     )
#     documents = loader.load()

#     new_documents = []
#     for doc in documents:
#         source = doc.metadata.get("source")
#         if source not in processed_files:
#             new_documents.append(doc)

#     return new_documents

# -------------------------------
# LOAD ONLY NEW TXT FILES
# -------------------------------
def load_new_txts(data_path):
    loader = DirectoryLoader(
        data_path,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    documents = loader.load()

    new_documents = []
    for doc in documents:
        source = doc.metadata.get("source")
        if source not in processed_files:
            new_documents.append(doc)

    return new_documents


# -------------------------------
# CREATE CHUNKS
# -------------------------------
def create_chunks(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    return splitter.split_documents(documents)


# -------------------------------
# EMBEDDING MODEL
# -------------------------------
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# -------------------------------
# LOAD NEW DOCUMENTS (change the function name accroding to pdf or text)
# -------------------------------
new_documents = load_new_txts(DATA_PATH)
print("📄 New pages found:", len(new_documents))

if not new_documents:
    print("✅ No new documents to process. Exiting.")
    exit()


# -------------------------------
# CREATE CHUNKS
# -------------------------------
chunks = create_chunks(new_documents)
print("✂️ New chunks created:", len(chunks))

if not chunks:
    raise ValueError("❌ PDFs loaded but no text chunks created (possibly scanned PDFs)")


# -------------------------------
# LOAD OR CREATE FAISS
# -------------------------------
if os.path.exists(DB_FAISS_PATH):
    print("🔁 Loading existing FAISS vector store...")
    db = FAISS.load_local(
        DB_FAISS_PATH,
        embedding_model,
        allow_dangerous_deserialization=True
    )
    db.add_documents(chunks)
else:
    print("🆕 Creating new FAISS vector store...")
    db = FAISS.from_documents(chunks, embedding_model)

db.save_local(DB_FAISS_PATH)

# -------------------------------
# UPDATE PROCESSED FILES
# -------------------------------
with open(PROCESSED_FILE, "a", encoding="utf-8") as f:
    for doc in new_documents:
        f.write(doc.metadata["source"] + "\n")

print("✅ Ingestion complete.")
