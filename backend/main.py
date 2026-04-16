import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from chatbot_backend import chatbot,get_lawyer_data
from langchain_core.messages import HumanMessage
from schemas import ChatRequest, ChatResponse
from datetime import datetime
from fastapi import HTTPException
from bson import ObjectId
from langchain_core.messages import HumanMessage, AIMessage
from database import conversation_collection


app = FastAPI()

# Allow React to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # later restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/new-chat")
async def new_chat(user_id: str):

    conversation = {
        "user_id": user_id,
        "created_at": datetime.utcnow(),
        "messages": []
    }

    result = await conversation_collection.insert_one(conversation)

    return {
        "conversation_id": str(result.inserted_id)
    }


# @app.post("/chat", response_model=ChatResponse)
# async def chat_endpoint(data: ChatRequest):
#     conversation_id = data.thread_id

#     # ✅ LOAD conversation history from MongoDB
#     conversation = await conversation_collection.find_one(
#         {"_id": ObjectId(conversation_id)}
#     )
    
#     if not conversation:
#         raise HTTPException(status_code=404, detail="Conversation not found")

#     # ✅ Convert MongoDB messages to LangChain format
    
#     history_messages = []
#     for msg in conversation.get("messages", []):
#         if msg["role"] == "user":
#             history_messages.append(HumanMessage(content=msg["content"]))
#         else:
#             history_messages.append(AIMessage(content=msg["content"]))
    
#     # Add current user message
#     history_messages.append(HumanMessage(content=data.message))

#     # Save USER message to MongoDB
#     await conversation_collection.update_one(
#         {"_id": ObjectId(conversation_id)},
#         {
#             "$push": {
#                 "messages": {
#                     "role": "user",
#                     "content": data.message,
#                     "timestamp": datetime.utcnow()
#                 }
#             }
#         }
#     )

#     # Call LangGraph with full history ✅
#     # config = {"configurable": {"thread_id": conversation_id}}

#     config = {
#     "configurable": {"thread_id": conversation_id},
#     "metadata": {
#         "thread_id": conversation_id
#     },
#     "run_name": "chat_turn",
#     }
    
#     ai_message = ""
#     for message_chunk, metadata in chatbot.stream(
#         {"messages": history_messages},  # ✅ Pass full history
#         config=config,
#         stream_mode="messages"
#     ):
#         # Only add content from AIMessage, ignore ToolMessage
#         if isinstance(message_chunk, AIMessage):
#             ai_message += message_chunk.content
#         lawyer_data = get_lawyer_data(ai_message["messages"])

#     # Save AI response
#     await conversation_collection.update_one(
#         {"_id": ObjectId(conversation_id)},
#         {
#             "$push": {
#                 "messages": {
#                     "role": "assistant",
#                     "content": ai_message,
#                     "timestamp": datetime.utcnow()
#                 }
#             }
#         }
#     )

#     return ChatResponse(
#         response=ai_message,
#         thread_id=conversation_id
#     )

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(data: ChatRequest):
    conversation_id = data.thread_id

    conversation = await conversation_collection.find_one(
        {"_id": ObjectId(conversation_id)}
    )
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    history_messages = []  # was missing

    for msg in conversation.get("messages", []):
        if msg["role"] == "user":
            history_messages.append(HumanMessage(content=msg["content"]))
        else:
            try:
                parsed = json.loads(msg["content"])
                if parsed.get("type") == "lawyer_results":
                    names = [l["name"] for l in parsed["lawyers"]]
                    history_messages.append(AIMessage(content=f"I recommended these lawyers: {', '.join(names)}"))
                else:
                    history_messages.append(AIMessage(content=msg["content"]))
            except:
                history_messages.append(AIMessage(content=msg["content"]))

    history_messages.append(HumanMessage(content=data.message))  # was missing

    await conversation_collection.update_one(
        {"_id": ObjectId(conversation_id)},
        {
            "$push": {
                "messages": {
                    "role": "user",
                    "content": data.message,
                    "timestamp": datetime.utcnow()
                }
            }
        }
    )

    config = {
        "configurable": {"thread_id": conversation_id},
        "metadata": {"thread_id": conversation_id},
        "run_name": "chat_turn",
    }
    
    ai_message = ""
    collected_messages = []

    for message_chunk, metadata in chatbot.stream(
        {"messages": history_messages},
        config=config,
        stream_mode="messages"
    ):
        collected_messages.append(message_chunk)
        if isinstance(message_chunk, AIMessage):
            ai_message += message_chunk.content

    lawyer_data = get_lawyer_data(collected_messages)  # was missing

    content_to_save = json.dumps(lawyer_data) if lawyer_data else ai_message

    await conversation_collection.update_one(
        {"_id": ObjectId(conversation_id)},
        {
            "$push": {
                "messages": {
                    "role": "assistant",
                    "content": content_to_save,
                    "timestamp": datetime.utcnow()
                }
            }
        }
    )

    return ChatResponse(
        response=ai_message,
        thread_id=conversation_id,
        lawyer_data=lawyer_data
    )

@app.get("/conversations/{user_id}")
async def get_user_conversations(user_id: str):
    """Fetch all conversations for a user"""
    conversations = await conversation_collection.find(
        {"user_id": user_id}
    ).sort("created_at", -1).to_list(length=100)  # Most recent first
    
    # Convert ObjectId to string
    for conv in conversations:
        conv["_id"] = str(conv["_id"])
    
    return conversations