import streamlit as st
from utils import extract_text, write_resume_md
from chains.dredge_chain import dredge
from chains.gen_chain import generate_resume

st.title("Auto-re-drafter")

job = st.text_area("Paste Job Posting")
cand_file = st.file_uploader("Candidate Doc (.pdf/.docx/.txt)", type=["pdf","docx","txt"])

if st.button("Generate Resume"):
    if not job or not cand_file:
        st.error("Missing info")
    else:
        with st.spinner("Extracting…"):
            cand_txt = extract_text(cand_file)
        with st.spinner("Finding facts"):
            facts = dredge(cand_txt, job)
        with st.spinner("Generating resume"):
            output = generate_resume(facts, job)
        resume_md, citations = output.split("# CITATIONS")
        write_resume_md(resume_md, "resume.docx")
        st.success("Download now")
        st.download_button("Resume (.docx)", "resume.docx")
        st.download_button("Citations (.pdf)", data=citations, file_name="citations.pdf", mime="application/pdf")
