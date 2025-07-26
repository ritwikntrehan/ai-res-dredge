import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import OpenAI

OPENAI_KEY = st.secrets["OPENAI_API_KEY"]

gen_prompt = PromptTemplate.from_file("prompts/gen_prompt.tpl")
gen_llm   = OpenAI(
    temperature=0.2,
    openai_api_key=OPENAI_KEY
)
gen_chain = LLMChain(llm=gen_llm, prompt=gen_prompt)

def generate_resume(facts_json: list, job_posting: str):
    return gen_chain.run(facts_json=facts_json, job_posting=job_posting)
