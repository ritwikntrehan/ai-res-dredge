from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI

# 1) Point to the new Jinja template:
rewrite_prompt = PromptTemplate(
    template_path="prompts/rewrite_resume.jinja",
    input_variables=["facts_json", "resume", "job_desc"],
    template_format="jinja2",
)

# 2) Initialize your LLM as before:
llm = OpenAI(
    temperature=0.7,
    model_name="gpt-4o-mini",     # or whichever model you’re using
)

# 3) Wire up the chain:
rewrite_chain = LLMChain(llm=llm, prompt=rewrite_prompt)

def rewrite_resume(facts_json: dict, resume: str, job_desc: str) -> str:
    """
    facts_json: the dict you extracted earlier
    resume: raw resume text
    job_desc: the pasted job description
    """
    return rewrite_chain.run(
        facts_json=facts_json,
        resume=resume,
        job_desc=job_desc,
    )
