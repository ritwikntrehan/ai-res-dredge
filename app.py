import io
import zipfile
import json
import pandas as pd
import streamlit as st
from chains import resume_chain  # hypothetical import
from utils import extract_facts, load_resume_bytes  # hypothetical helpers

# Streamlit app entrypoint
def main():
    st.title("AI Resume Redraft")

    # --- Inputs ---
    uploaded_file = st.file_uploader("Upload your resume (.docx)", type=["docx"])
    job_desc = st.text_area("Paste the job description here")
    num_docs = st.slider("Number of retrieval docs", 1, 10, 5)
    temp = st.slider("Generation temperature", 0.0, 1.0, 0.7)

    if uploaded_file and job_desc:
        # Load resume bytes
        resume_bytes = load_resume_bytes(uploaded_file)

        # Extract facts via RAG chain
        facts_json = extract_facts(resume_bytes, job_desc, num_docs)

        # Generate rewritten resume and capture tokens
        rewritten_resume, tokens, token_mapping = resume_chain(
            resume_bytes,
            job_desc,
            num_docs=num_docs,
            temperature=temp,
            return_tokens=True,
        )

        # --- Debug Outputs ---
        with st.expander("🛠️ Debug: Extracted Facts", expanded=False):
            st.json(facts_json)

        with st.expander("🛠️ Debug: All Output Tokens", expanded=False):
            # tokens is a list of token strings
            st.write(tokens)

        # Build a DataFrame for token-to-placement mapping
        if token_mapping:
            mapping_df = pd.DataFrame.from_dict(
                token_mapping,
                orient="index",
                columns=["Section", "Char Position"]
            ).reset_index().rename(columns={"index": "Token Index"})

            with st.expander("🛠️ Debug: Token ↔️ Placement Mapping", expanded=False):
                st.dataframe(mapping_df)

        # Show rewritten resume preview
        st.subheader("Rewritten Resume Preview")
        st.download_button(
            label="📥 Download All Outputs",
            data=_make_zip(facts_json, resume_bytes),
            file_name="ai_res_dredge_outputs.zip",
            mime="application/zip"
        )

    else:
        st.info("Please upload a resume and paste a job description to get started.")


def _make_zip(facts_json, resume_bytes):
    """
    Prepare an in-memory ZIP with facts.json and resume.docx
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as z:
        # Add facts.json
        z.writestr("facts.json", json.dumps(facts_json, indent=2))
        # Add rewritten resume
        z.writestr("resume.docx", resume_bytes)

    zip_buffer.seek(0)
    return zip_buffer.getvalue()


if __name__ == "__main__":
    main()
