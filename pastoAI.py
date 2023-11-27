# All library imports
import os
import shutil
import streamlit as st
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from langchain.document_loaders import *
from langchain.chains.summarize import load_summarize_chain
import tempfile
from langchain.docstore.document import Document
import time
from langchain.memory import ConversationBufferMemory
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Get openai_api_key
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)

st.title('noBatery')

# Copy and paste all the functions as is
def grassCuttingPlanner(grass_area_size,battery_status):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0
    )
    system_template = """You are an AI assistant designed to generate an efficient plan for cutting grass considering the battery status."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """The size of the grass area is {grass_area_size} and the current battery status is {battery_status}. Please generate an efficient plan for cutting the grass."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(grass_area_size=grass_area_size, battery_status=battery_status)
    return result # returns string   

# Create a form
with st.form(key='grass_cutting_planner'):
    # Under the form, take all the user inputs
    grass_area_size = st.number_input("Enter the size of the grass area")
    battery_status = st.text_input("Enter the battery status of the lawn mower")
    submit_button = st.form_submit_button(label='Generate Plan')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            cutting_plan = ""
        elif grass_area_size and battery_status:
            cutting_plan = grassCuttingPlanner(grass_area_size,battery_status)
        else:
            cutting_plan = ""
        # Under the st.form_submit_button, show the results.
        if cutting_plan:
            st.table(cutting_plan)