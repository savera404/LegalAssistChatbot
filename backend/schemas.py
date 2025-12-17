from pydantic import BaseModel
from typing import List

class ChatRequest(BaseModel):
    message: str
    thread_id: str

class ChatResponse(BaseModel):
    response: str
    thread_id: str
