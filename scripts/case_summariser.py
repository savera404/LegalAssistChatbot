from langchain_community.document_loaders import PyPDFLoader
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv

load_dotenv()
api_key=os.getenv('GROQ_API_KEY')

INPUT_DIR = r"D:\LegalAssist_chatbot\data\cases"
OUTPUT_DIR = r'D:\LegalAssist_chatbot\data\case_summaries'
PROCESSED_FILE = r'data\processed_cases.txt'

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs("data", exist_ok=True)


# -----------------------------
# Processed cases tracking
# -----------------------------
def load_processed_cases(path=PROCESSED_FILE):
    if not os.path.exists(path):
        return set()
    with open(path, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())


def mark_case_processed(filename, path=PROCESSED_FILE):
    with open(path, "a", encoding="utf-8") as f:
        f.write(filename + "\n")


# -----------------------------
# PDF text extraction
# -----------------------------
def extract_pdf_text(pdf_path):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    return "\n".join([doc.page_content for doc in docs])


# -----------------------------
# Summarization prompt
# -----------------------------
SUMMARY_PROMPT = """
You are a legal assistant specializing in Pakistani law.

Summarize the following court judgment STRICTLY in this format:

Case Name:
Court:
Year:
Legal Issue:
Relevant Law / Sections:
Key Facts (brief):
Holding / Decision:
Legal Principle Established:

Rules:
- Do NOT invent facts.
- If information is unclear, write "Not specified".
- Keep it concise and factual.
- Use neutral legal language.
"""


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY")
)


def summarize_case(case_text):
    response = llm.invoke([
        HumanMessage(content=SUMMARY_PROMPT + "\n\n" + case_text[:12000])
    ])
    return response.content


def save_summary_txt(summary, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(summary)


# -----------------------------
# MAIN PIPELINE
# -----------------------------
processed_cases = load_processed_cases()

for file in os.listdir(INPUT_DIR):
    if not file.endswith(".pdf"):
        continue

    if file in processed_cases:
        print(f"⏭️ Skipping already summarized: {file}")
        continue

    print(f"🆕 Processing: {file}")

    pdf_path = os.path.join(INPUT_DIR, file)
    case_text = extract_pdf_text(pdf_path)
    summary = summarize_case(case_text)

    output_file = file.replace(".pdf", "_summary.txt")
    save_summary_txt(summary, os.path.join(OUTPUT_DIR, output_file))

    mark_case_processed(file)

print("✅ Case summarization completed")
