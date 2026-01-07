from langgraph.graph import StateGraph, START,END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage,AIMessage, SystemMessage
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from groq import Groq
import os
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode,tools_condition
from rag_tool import rag_tool

load_dotenv()
api_key=os.getenv('GROQ_API_KEY')
client=Groq()

#llm definition
llm = ChatGroq(
    model="openai/gpt-oss-20b", 
    temperature=0,
    groq_api_key=api_key
    
)
LEGAL_SYSTEM_PROMPT = """
You are Adil AI, an AI legal assistant specialized in Pakistani law.

CRITICAL INSTRUCTIONS:
1. You MUST call the rag_tool before answering ANY legal question
2. After receiving tool results, you MUST base your answer on the retrieved documents
3. Use the SOURCE information and content from the tool to answer accurately

Rules:
- Answer ONLY questions related to Pakistani law.
- If a question is outside Pakistani law, politely refuse and redirect
- Use very simple, clear language understandable by non-lawyers, do not use complex legal language or complex vocabulary
- Always cite laws and cases by name, section, and year in plain text. 
- Do NOT use placeholders like [1†source].


When answering a user’s question:

• First, explain the applicable Pakistani law clearly and concisely based only on the retrieved legal documents.
• If one or more relevant court cases are present in the retrieved context and directly relate to the user’s situation, briefly mention the case(s) and explain how the legal principle from the case applies.
• Do NOT invent or assume case law.
• If no relevant case law is found in the retrieved documents, answer using statutory law only and do not mention any cases.
• Always base your answer strictly on the provided context.

"""
#gather all tools here
tools=[rag_tool]
llm_with_tools=llm.bind_tools(tools)


#state definition
class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage], add_messages]

#function definitions
#chat node
def chat_node(state:ChatState):
    messages=state['messages']

        # Ensure system prompt is always first
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=LEGAL_SYSTEM_PROMPT)] + messages

    response=llm_with_tools.invoke(messages)
    return {'messages':[response]}

#tool node
tool_node=ToolNode(tools)



#graph definition
graph=StateGraph(ChatState)

graph.add_node('chat_node',chat_node)
graph.add_node('tools',tool_node)

graph.add_edge(START,'chat_node')
graph.add_conditional_edges('chat_node',tools_condition)
graph.add_edge('tools','chat_node')

# graph.add_edge('chat_node',END)

checkpointer=MemorySaver()
chatbot=graph.compile()

# initial_state={
#     'messages':[HumanMessage(content='What is the capital of Pakistan?')]
# }
# print(chatbot.invoke(initial_state)['messages'][-1].content)

# thread_id=1
# while True:
#     user_message=input('Type here: ')
#     print('You: ',user_message)

#     if user_message.strip().lower() in ['exit','quit','bye']:
#         break

#     config={'configurable':{'thread_id':thread_id}}
#     response=chatbot.invoke({'messages': [HumanMessage(content=user_message)]}, config=config)

#     print("ChatBot: ", response['messages'][-1].content)