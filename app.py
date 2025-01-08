from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os

# Initialize session state for API key if not already present
if 'api_key_configured' not in st.session_state:
    st.session_state.api_key_configured = False

# Sidebar for API configuration
st.sidebar.header("API Configuration")

# API key input in sidebar
langchain_api_key = st.sidebar.text_input("Enter your Langchain API Key", type="password")

# Button to save API key
if st.sidebar.button("Save API Key"):
    if langchain_api_key:
        os.environ["LANGCHAIN_API_KEY"] = langchain_api_key
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_PROJECT"] = "pr-rundown-stab-27"
        st.session_state.api_key_configured = True
        st.sidebar.success("API Key saved successfully!")
    else:
        st.sidebar.error("Please enter an API key")

# Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Please respond to the user queries"),
    ("user", "Question:{question}")
])

def generate_response(question, engine, temperature, max_tokens):
    llm = Ollama(model=engine)
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    answer = chain.invoke({"question": question})
    return answer

# Main app interface
st.title("AI Question Answering App ")

# Model selection and parameters in sidebar
st.sidebar.header("Model Configuration")
engine = st.sidebar.selectbox("Select an Open AI Model", ["gemma2:2b"])
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("max_Tokens", min_value=50, max_value=300, value=150)

# Main interface for user input
st.write("Go ahead and ask any question")
user_input = st.text_input("You:")

# Generate response only if API key is configured and there's user input
if user_input:
    if st.session_state.api_key_configured:
        response = generate_response(user_input, engine, temperature, max_tokens)
        st.write(response)
    else:
        st.error("Please configure your API key in the sidebar first")
else:
    st.write("Please provide the user input")
