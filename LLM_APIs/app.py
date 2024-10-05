import vertexai
import sys
from vertexai.generative_models import GenerativeModel, Part
import vertexai.generative_models as generative_models
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain_google_vertexai import VertexAI

import streamlit as st
import os

def init():
    if "chain" not in st.session_state:
        model = VertexAI(model_name="gemini-pro")
        memory = ConversationBufferMemory()
        chain = ConversationChain(llm=model, memory = memory)
        st.session_state['chain'] = chain
    
init()
    
chain = st.session_state.chain
## function to load Gemini Pro model and get repsonses
def get_gemini_response(question):
    
    response=chain(question)
    return response

##initialize our streamlit app

st.set_page_config(page_title="Q&A Demo")

st.header("Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input=st.text_input("Input: ",key="input")
submit=st.button("Ask the question")

if submit and input:
    response=get_gemini_response(input)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The Response is")
    st.write(response['response'])
    st.session_state['chat_history'].append(("Bot", response['response']))
        
st.subheader("The Chat History is")
    
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")

