import docx2txt
from io import BytesIO

def load_resume_text(resume_file):
    """
    Load and return the full text of the user’s resume.
    - If they uploaded a .docx (Streamlit UploadedFile), run it through docx2txt.
    - Otherwise, treat it as plain text.
    """
    if not resume_file:
        return ""
    # read raw bytes from the uploader
    raw = resume_file.read()
    # try .docx first
    try:
        return docx2txt.process(BytesIO(raw))
    except Exception:
        # fallback to utf‑8 text
        try:
            return raw.decode("utf‑8")
        except:
            return str(raw)

def load_job_description(jd_input):
    """
    Return the job description text.
    - If they uploaded a file, read & decode.
    - Otherwise assume it’s a plain string.
    """
    # Streamlit’s text_area will give you a str, so just return it
    if isinstance(jd_input, str):
        return jd_input
    # else it’s probably an UploadedFile
    raw = jd_input.read()
    try:
        return raw.decode("utf‑8")
    except:
        # maybe it’s a .docx
        return docx2txt.process(BytesIO(raw))
