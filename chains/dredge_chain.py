# chains/dredge_chain.py
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI

key = st.secrets["OPENAI_API_KEY"]
dredge_prompt = PromptTemplate.from_file("prompts/dredge_prompt.tpl")
dredge_llm   = OpenAI(temperature=0.0, openai_api_key=key)
dredge_chain = LLMChain(llm=dredge_llm, prompt=dredge_prompt)
