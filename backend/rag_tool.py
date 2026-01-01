
from langchain_core.tools import tool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv


load_dotenv()

DB_FAISS_PATH = r"D:\LegalAssist_chatbot\vectorstore\faiss_store"


embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(
    DB_FAISS_PATH,
    embedding_model,
    allow_dangerous_deserialization=True
)
retriever = db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)
# print(retriever.invoke("Tell me about Muslim marriage laws"))
#rag tool

@tool
def rag_tool(query):

    """
    Retrieve relevant Pakistani legal documents from the knowledge base
    based on the user's query. Use this tool to answer questions related
    to Pakistan's family laws and women's rights.
    """

    result=retriever.invoke(query)

    context_blocks=[]

    content=[doc.page_content for doc in result]
    source=[doc.metadata.get('source') for doc in result]

    context_blocks.append(
    f"[SOURCE: {source}]\n{content}"
)


    return "\n\n".join(context_blocks)




