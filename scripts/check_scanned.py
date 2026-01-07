import os
from langchain_community.document_loaders import PyPDFLoader
from collections import defaultdict


DATA_PATH = r"D:\LegalAssist_chatbot\data\cases"
MIN_TEXT_LENGTH = 200   # threshold


def check_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    total_text = ""
    for doc in documents:
        total_text += doc.page_content.strip()

    return {
        "file": os.path.basename(pdf_path),
        "pages": len(documents),
        "text_length": len(total_text),
        "is_scanned": len(total_text) < MIN_TEXT_LENGTH
    }


def main():
    print("\n🔍 SCANNED PDF CHECK REPORT\n")

    for file in os.listdir(DATA_PATH):
        if file.lower().endswith(".pdf"):
            pdf_path = os.path.join(DATA_PATH, file)

            try:
                result = check_pdf(pdf_path)

                status = "⚠️ SCANNED" if result["is_scanned"] else "✅ TEXT PDF"

                print(f"{status}")
                print(f"📄 File        : {result['file']}")
                print(f"📑 Pages      : {result['pages']}")
                print(f"🧾 Text chars : {result['text_length']}")
                print("-" * 50)

            except Exception as e:
                print(f"❌ ERROR reading {file}: {e}")
                print("-" * 50)


if __name__ == "__main__":
    main()
