from pathlib import Path
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import json

def get_facts_extraction_chain(
    temperature: float = 0.0,
    model_name: str = "gpt-4o-mini"
) -> LLMChain:
    template_str = Path("prompts/facts_extraction_template.txt").read_text(encoding="utf-8")
    prompt = PromptTemplate(
        template=template_str,
        input_variables=["resume_text"],
        template_format="jinja2",
    )
    llm = ChatOpenAI(
        model=model_name,
        temperature=temperature,
        max_tokens=500
    )
    return LLMChain(llm=llm, prompt=prompt)

def extract_facts(resume_text: str) -> dict:
    chain = get_facts_extraction_chain()
    result = chain.invoke({"resume_text": resume_text})
    # The chain returns JSON text
    try:
        return json.loads(result.generations[0][0].text)
    except json.JSONDecodeError:
        # fallback to empty structure
        return {"certification": "", "coursework": [], "skills": [], "tools": []}
