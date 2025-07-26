from pathlib import Path
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

def get_resume_rewrite_chain(
    temperature: float = 0.7,
    max_tokens: int = 800,
    model_name: str = "gpt-4o-mini"
) -> LLMChain:
    template_str = Path("prompts/rewrite_template.txt").read_text(encoding="utf-8")
    prompt = PromptTemplate(
        template=template_str,
        input_variables=["resume", "job_description", "facts_json"],
        template_format="jinja2",
    )
    llm = ChatOpenAI(
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return LLMChain(llm=llm, prompt=prompt)
