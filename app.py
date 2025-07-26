import streamlit as st
from utils import load_resume_text, load_job_description
from chains.extraction_chain import extract_facts  # your existing extraction logic
from chains.rewrite_chain import rewrite_resume      # new rewrite function

st.set_page_config(page_title="Auto Res Redraft", layout="wide")
st.title("Auto Res Redraft")

# 1. Upload / paste resume
st.sidebar.header("Upload your resume")
resume_file = st.sidebar.file_uploader("Upload .docx or .txt", type=["docx", "txt"])
resume_text = load_resume_text(resume_file) if resume_file else st.sidebar.text_area("Or paste resume here")

# 2. Paste job description
st.sidebar.header("Target Job Description")
job_desc = st.sidebar.text_area("Paste the JD here")

# 3. Parameters
st.sidebar.header("RAG & LLM Settings")
k = st.sidebar.slider("Number of retrieved chunks (k)", 1, 10, 5)
temperature = st.sidebar.slider("LLM temperature", 0.0, 1.0, 0.7)

# 4. Run extraction + rewrite
if st.button("🔄 Rewrite Resume"):
    with st.spinner("Extracting facts…"):
        facts_json = extract_facts(resume_text)
    st.markdown("**Extracted facts:**")
    st.json(facts_json)

    with st.spinner("Generating tailored bullets…"):
        rewritten = rewrite_resume(
            facts_json=facts_json,
            resume=resume_text,
            job_desc=job_desc
        )
    st.markdown("**✔️ Rewritten Resume Bullets:**")
    st.write(rewritten)
