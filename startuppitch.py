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

st.title('Startup Pitch')

# Copy and paste all the functions as is
def startupPitchGenerator(startup_pitch):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are an assistant designed to generate a phrase similar to 'the uber of...' using the given startup pitch: '{startup_pitch}'."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Based on the startup pitch: '{startup_pitch}', please generate a phrase similar to 'the uber of...'."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(startup_pitch=startup_pitch)
    return result # returns string   

# Create a form
with st.form(key='startup_pitch_form'):
    # Under the form, take all the user inputs
    startup_pitch = st.text_area("Enter your startup pitch")
    submit_button = st.form_submit_button(label='Generate Phrase')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            uber_phrase = ""
        elif startup_pitch:
            uber_phrase = startupPitchGenerator(startup_pitch)
        else:
            uber_phrase = ""
        # Under the st.form_submit_button, show the results.
        if uber_phrase:
            st.text(uber_phrase)