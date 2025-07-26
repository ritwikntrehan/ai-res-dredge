import os
import json
import docx2txt
import PyPDF2
import openai
from chains.facts_extraction_chain import extract_facts

# Initialize OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY", "")

def parse_resume_file(uploaded_file) -> str:
    """
    Read a Streamlit-uploaded resume file (PDF, DOCX/DOC, or TXT) and return its plain text.
    """
    # Determine content type or file extension fallback
    content_type = getattr(uploaded_file, "type", "")
    filename = getattr(uploaded_file, "name", "")
    lower_name = filename.lower()

    # Handle PDF files
    if content_type == "application/pdf" or lower_name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(uploaded_file)
        text_pages = []
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text_pages.append(page_text)
        return "\n".join(text_pages).strip()

    # Handle DOCX/DOC files
    if (content_type in (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/msword"
        ) or lower_name.endswith((".docx", ".doc"))):
        return docx2txt.process(uploaded_file)

    # Handle plain text files
    if content_type == "text/plain" or lower_name.endswith(".txt"):
        try:
            raw = uploaded_file.getvalue()
            if isinstance(raw, (bytes, bytearray)):
                return raw.decode("utf-8", errors="ignore")
            return str(raw)
        except Exception:
            return ""

    # Fallback: try to decode raw bytes from unknown types
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
    facts = extract_facts(resume_text)
    # Ensure valid structure
    return {
        "certification": facts.get("certification", ""),
        "coursework": facts.get("coursework", []),
        "skills": facts.get("skills", []),
        "tools": facts.get("tools", []),
    }
