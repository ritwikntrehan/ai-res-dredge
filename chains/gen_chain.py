# chains/gen_chain.py
import os
from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI

gen_prompt = PromptTemplate.from_file("prompts/gen_prompt.tpl")
gen_llm   = OpenAI(temperature=0.2, openai_api_key=os.getenv("OPENAI_API_KEY"))
gen_chain = LLMChain(llm=gen_llm, prompt=gen_prompt)

def generate_resume(facts_json: list, job_posting: str):
    return gen_chain.run(facts_json=json.dumps(facts_json), job_posting=job_posting)
