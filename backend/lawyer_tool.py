from langchain_core.tools import tool
import asyncio
from database import db

def extract_practice_areas(query: str):
    query = query.lower()

    if "divorce" in query or "khula" in query or "custody" in query:
        return ["family"]

    if "inheritance" in query or "property" in query:
        return ["family", "property"]

    if "harassment" in query:
        return ["criminal"]


    return ["family"]

@tool

def lawyer_tool(query: str) -> str:
    """
    Use this tool when the user asks for a lawyer, legal help, or recommendations.
    Input should describe the case type (e.g., divorce, custody, harassment).
    """
    
    practice_areas = extract_practice_areas(query)

    lawyers = list(db['lawyers'].find({
        "practiceArea": {"$in": practice_areas}  # camelCase singular, matches schema
    }).limit(5))

    if not lawyers:
        return "Sorry, no lawyers found for your case."

    response = "Here are some lawyers you can consult:\n"
    for l in lawyers:
        response += (
            f"• {l['firstName']} {l['lastName']} - {l.get('practiceArea', 'N/A')}\n"
            f"  City: {l.get('city', 'N/A')}, "
            f"Experience: {l.get('experience', 'N/A')} years\n\n"
        )

    return response