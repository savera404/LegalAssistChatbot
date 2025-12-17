from langgraph.graph import StateGraph, START,END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage,AIMessage
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from groq import Groq
import os
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()
api_key=os.getenv('GROQ_API_KEY')
client=Groq()

#llm definition
llm = ChatGroq(
    model="openai/gpt-oss-20b", 
    temperature=0,
    groq_api_key=api_key
    
)

#state definition
class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage], add_messages]

#function definitions
def chat_node(state:ChatState):
    messages=state['messages']
    response=llm.invoke(messages)
    return {'messages':[response]}


#graph definition
graph=StateGraph(ChatState)

graph.add_node('chat_node',chat_node)

graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

checkpointer=MemorySaver()
chatbot=graph.compile(checkpointer=checkpointer)

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