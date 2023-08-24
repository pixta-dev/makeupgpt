import os
os.environ["OPENAI_API_KEY"] = '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'


import streamlit as st
import random
import time
from engine import Engine

# Tracking with ClearML
from clearml import Task
task = Task.init(project_name='Face Makeup', task_name='Sample Retrieval')



st.title("MakeupGPT")

# Input User Data
st.header("User Data")
user_data = st.text_area("Say something")

if user_data:
    st.write("User data loaded")

st.divider()

# Advice
st.header("Advice")
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if context := st.chat_input("What would you like to makeup for? "):
    with st.spinner("I'm thinking"):
        # Add user message to chat history
        llm = Engine(users_data=user_data, context_data=context)
        guide = llm.create_advice()
        print(guide)
        advice = llm.create_advice_with_prod()
        print(advice)
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(context)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            full_response += advice
            message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

