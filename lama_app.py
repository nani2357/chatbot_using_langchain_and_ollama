from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")

## Initialize session state for conversation history
if 'history' not in st.session_state:
    st.session_state['history'] = []

## Prompt Template
def create_prompt(messages):
    return ChatPromptTemplate.from_messages(
        [("system", "You are a helpful assistant. Please respond to the user queries")] + messages
    )

## Streamlit UI
st.title('Langchain Demo With LLAMA2 API')
input_text = st.text_input("Search the topic you want", key="query")

# Initialize LLAMA model
llm = Ollama(model="llama3")
output_parser = StrOutputParser()

# Handle new input
if input_text:
    # Append user input to history
    st.session_state['history'].append(("user", f"Question:{input_text}"))

    # Create prompt with current history
    prompt = create_prompt(st.session_state['history'])
    chain = prompt | llm | output_parser

    # Invoke the model
    output = chain.invoke({"question": input_text})
    
    # Display the output and update history
    st.write(output)
    st.session_state['history'].append(("system", output))

# Clear button to reset conversation
if st.button('Clear Conversation'):
    st.session_state['history'] = []