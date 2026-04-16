from langchain_core.tools import tool
import json
from database import db

def extract_practice_areas(query: str):
    query = query.lower()

    if "divorce" in query or "khula" in query or "custody" in query:
        return ["family"]

    if "inheritance" in query or "property" in query:
        return ["family", "property"]

    if "harassment" in query:
        return ["criminal"]
    
    if "all lawyers" in query:
        return ['family', 'criminal', 'corporate', 'property']


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

    result = {
        "type": "lawyer_results",
        "lawyers": [
            {
                "id": str(l["_id"]),
                "name": f"{l['firstName']} {l['lastName']}",
                "practiceArea": l.get("practiceArea", "N/A"),
                "city": l.get("city", "N/A"),
                "experience": l.get("experience", "N/A"),
            }
            for l in lawyers
        ]
    }
    return json.dumps(result)