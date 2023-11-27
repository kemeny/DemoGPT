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
import markdown

# Get openai_api_key
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)

# Copy and paste all the functions as is
def load_file(file_path):
    loader = UnstructuredPDFLoader(file_path, mode="elements", strategy="fast")
    docs = loader.load()
    return docs

def contentGenerator(file_str,content_type):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
        temperature=0.7
    )
    system_template = """You are an assistant designed to generate content based on the given file content and content type."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """The file content is: '{file_str}', and the content type is: '{content_type}'. Please generate the appropriate content."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(file_str=file_str, content_type=content_type)
    return result # returns string   

def format_markdown(content):
    return markdown.markdown(content)

# Create a form
with st.form(key='content_maker'):
    # Under the form, take all the user inputs
    uploaded_file = st.file_uploader("Upload PDF File", type=["pdf"], key='file_path')
    content_type = st.text_input("Enter the content type")
    submit_button = st.form_submit_button(label='Generate Content')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        if uploaded_file is not None:
            # Create a temporary file to store the uploaded content
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(uploaded_file.read())
                file_path = temp_file.name # it shows the file path
        else:
            file_path = ''
        if file_path:
            file_doc = load_file(file_path)
        else:
            file_doc = ''
        file_str = "".join([doc.page_content for doc in file_doc])
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            content = ""
        elif file_str and content_type:
            content = contentGenerator(file_str,content_type)
        else:
            content = ""
        markdown_content = format_markdown(content)
        # Under the st.form_submit_button, show the results.
        if markdown_content:
            st.markdown(markdown_content)