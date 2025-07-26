# chains/dredge_chain.py
from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI

dredge_prompt = PromptTemplate.from_file("prompts/dredge_prompt.tpl")
dredge_llm   = OpenAI(temperature=0.0, openai_api_key=os.getenv("OPENAI_API_KEY"))
dredge_chain = LLMChain(llm=dredge_llm, prompt=dredge_prompt)

def dredge(candidate_text: str, job_posting: str):
    resp = dredge_chain.run(candidate_text=candidate_text, job_posting=job_posting)
    return json.loads(resp)
