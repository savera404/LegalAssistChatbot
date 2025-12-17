from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from chatbot_backend import chatbot
from langchain_core.messages import HumanMessage
from schemas import ChatRequest, ChatResponse
import uuid

app = FastAPI()

# Allow React to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(data: ChatRequest):

    config = {"configurable": {"thread_id": data.thread_id}}

    ai_message = ""
    for message_chunk, _ in chatbot.stream(
        {"messages": [HumanMessage(data.message)]},
        config=config,
        stream_mode="messages"
    ):
        ai_message += message_chunk.content

    return ChatResponse(
        response=ai_message,
        thread_id=data.thread_id
    )


@app.get("/history/{thread_id}")
def get_history(thread_id: str):
    state = chatbot.get_state(
        config={"configurable": {"thread_id": thread_id}}
    )

    messages = []
    for msg in state.values.get("messages", []):
        role = "user" if msg.type == "human" else "assistant"
        messages.append({
            "role": role,
            "content": msg.content
        })

    return messages
