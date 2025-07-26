import os, io, streamlit as st
from utils import extract_text, write_resume_md
from chains.dredge_chain import dredge
from chains.gen_chain import generate_resume

st.set_page_config(page_title="Auto‑re‑drafter v0.1")
st.title("Auto‑re‑drafter (v0.1)")

# --- INPUTS --------------------------------------------------------------
job = st.text_area("Paste Job Posting", height=200)

cand_files = st.file_uploader(
    "Candidate docs (resume, certs, transcript, analyst notes …)",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
)

# --- GENERATE ------------------------------------------------------------
if st.button("Generate résumé"):
    if not job or not cand_files:
        st.error("Please provide the job posting **and** at least one candidate file.")
    else:
        # 1) concat all uploaded docs
        with st.spinner("Extracting text …"):
            cand_txt = "\n\n".join(extract_text(f) for f in cand_files)

        # 2) dredge → facts JSON
        with st.spinner("Dredging facts …"):
            facts = dredge(cand_txt, job)

        # 3) generate résumé + citations
        with st.spinner("Drafting résumé …"):
            output = generate_resume(facts, job)

        # 4) split safely
        resume_md, citations = (output.split("# CITATIONS", 1) + [""])[:2]
        resume_md = resume_md.strip()
        citations  = citations.strip() or "LLM did not return a citation section."

        # 5) write résumé file
        resume_path = "resume.docx"
        write_resume_md(resume_md, resume_path)

        # 6) save citations to bytes (txt for now; swap in real PDF later)
        citations_bytes = citations.encode("utf‑8")

        # 7) stash in session_state so buttons persist across rerun
        st.session_state["resume_path"] = resume_path
        st.session_state["citations_bytes"] = citations_bytes

        st.success("Files ready ↓")

# --- DOWNLOAD BUTTONS ----------------------------------------------------
if "resume_path" in st.session_state:
    with open(st.session_state["resume_path"], "rb") as f:
        st.download_button(
            "Download résumé (.docx)",
            f,
            file_name="resume.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            key="resume_dl",
        )

if "citations_bytes" in st.session_state:
    st.download_button(
        "Download citations (.txt)",
        st.session_state["citations_bytes"],
        file_name="citations.txt",
        mime="text/plain",
        key="cites_dl",
    )
