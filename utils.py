import os
import json
import docx2txt
import PyPDF2
import openai
from chains.facts_extraction_chain import extract_facts as chain_extract_facts

# Initialize OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY", "")

def parse_resume_file(uploaded_file) -> str:
    """
    Read a Streamlit-uploaded resume file (PDF, DOCX/DOC, or TXT) and return its plain text.
    """
    content_type = getattr(uploaded_file, "type", "")
    filename = getattr(uploaded_file, "name", "")
    lower_name = filename.lower()

    # Handle PDF files
    if content_type == "application/pdf" or lower_name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(uploaded_file)
        text_pages = []
        for page in reader.pages:
            text_pages.append(page.extract_text() or "")
        return "\n".join(text_pages).strip()

    # Handle DOCX/DOC files
    if (
        content_type in (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/msword"
        ) or lower_name.endswith(('.docx', '.doc'))
    ):
        return docx2txt.process(uploaded_file)

    # Handle plain text files
    if content_type == "text/plain" or lower_name.endswith('.txt'):
        try:
            raw = uploaded_file.getvalue()
            if isinstance(raw, (bytes, bytearray)):
                return raw.decode("utf-8", errors="ignore")
            return str(raw)
        except Exception:
            return ""

    # Fallback: decode raw bytes
    try:
        raw = uploaded_file.getvalue()
        if isinstance(raw, (bytes, bytearray)):
            return raw.decode("utf-8", errors="ignore")
        return str(raw)
    except Exception:
        return ""


def extract_facts(resume_text: str) -> dict:
    """
    Extract structured facts from the resume text using the LLM-based extraction chain.

    Returns a dictionary with keys:
      - certification: str
      - coursework: list[str]
      - skills: list[str]
      - tools: list[str]
    """
    facts = chain_extract_facts(resume_text)
    return {
        "certification": facts.get("certification", ""),
        "coursework": facts.get("coursework", []),
        "skills": facts.get("skills", []),
        "tools": facts.get("tools", []),
    }
