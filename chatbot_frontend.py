import streamlit as st
from chatbot_backend import chatbot
from langchain_core.messages import HumanMessage
import uuid

#utility functions

def generate_thread_id():
    thread_id=uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id=generate_thread_id()
    st.session_state['thread_id']=thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history']=[]

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    state_snapshot = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    state_values = state_snapshot.values  
    return state_values.get('messages', [])


#session_management
if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]

if 'thread_id' not in st.session_state:
    st.session_state['thread_id']=generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads']=[]
add_thread(st.session_state['thread_id'])

#sidebar UI
st.sidebar.title("LangGraph Chatbot")


if st.sidebar.button("Start New Chat"):
    reset_chat()

st.sidebar.header('Past Conversations')

for thread_id in st.session_state['chat_threads']:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id']=thread_id
        messages=load_conversation(thread_id)

        temp_messages=[]
        for msg in messages:
            if isinstance(msg,HumanMessage):
                role='user'
            else:
                role='AI'
            temp_messages.append({'role':role,'content': msg.content})
        st.session_state['message_history']=temp_messages
    


#loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input=st.chat_input("Type Here")

CONFIG={'configurable':{'thread_id':st.session_state['thread_id']}}

if user_input:

    #first add message to message_history
    st.session_state['message_history'].append({"role":"user","content":user_input})
    with st.chat_message('user'):
        st.text(user_input)
    

    #assistant message with streaming implemented
    with st.chat_message("assistant"):
        ai_message=st.write_stream(
            message_chunk.content for message_chunk,metadata in chatbot.stream(
                {"messages":[HumanMessage(user_input)]},
                config=CONFIG,
                stream_mode="messages"
            )
        )
    st.session_state['message_history'].append({"role":"assistant","content":ai_message})