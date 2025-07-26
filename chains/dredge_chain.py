import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import OpenAI     # use community provider

# grab your key from Streamlit secrets
OPENAI_KEY = st.secrets["OPENAI_API_KEY"]

dredge_prompt = PromptTemplate.from_file("prompts/dredge_prompt.tpl")
dredge_llm   = OpenAI(
    temperature=0.0,
    openai_api_key=OPENAI_KEY
)
dredge_chain = LLMChain(llm=dredge_llm, prompt=dredge_prompt)

def dredge(candidate_text: str, job_posting: str):
    return dredge_chain.run(candidate_text=candidate_text, job_posting=job_posting)
