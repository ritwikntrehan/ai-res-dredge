import docx2txt
import PyPDF2
import openai
import os
from chains.facts_extraction_chain import extract_facts

openai.api_key = os.getenv("OPENAI_API_KEY", "")

def parse_resume_file(uploaded_file) -> str:
    """
    Read a Streamlit-uploaded file (PDF or DOCX) and return plain text.
    """
    content_type = uploaded_file.type
    if content_type == "application/pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    elif content_type in (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword"
    ):
        return docx2txt.process(uploaded_file)
    else:
        # fallback: try reading raw bytes
        return uploaded_file.getvalue().decode("utf-8", errors="ignore")

# Re-export extract_facts from your chain module
# def extract_facts(resume_text: str) -> dict:
#     ...
