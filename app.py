import streamlit as st
import json
import io
import sys, os
from zipfile import ZipFile
from chains.rag_chain import ResumeRAGChain

sys.path.append(os.path.abspath("src"))

# Initialize RAG chain
chain = ResumeRAGChain()

st.title("AI Resume Redraft")

# User inputs
uploaded_resume = st.file_uploader("Upload your current resume", type=["docx", "pdf"])
job_desc = st.text_area("Paste the target job description here")

# Parameters
top_k = st.slider("Number of retrieved facts", 1, 10, 5)
temperature = st.slider("Generation temperature", 0.0, 1.0, 0.7)

if st.button("Rewrite"):    
    if not uploaded_resume or not job_desc:
        st.error("Please provide both a resume and a job description.")
    else:
        with st.spinner("Generating draft..."):
            # Run chain: returns dict with 'facts_json', 'output_tokens', 'resume_docx'
            result = chain.run(
                resume_file=uploaded_resume,
                job_description=job_desc,
                top_k=top_k,
                temperature=temperature
            )

        # Debug outputs for troubleshooting
        st.subheader("Extracted Facts JSON (debug)")
        st.json(result.get('facts_json', {}))

        st.subheader("All Output Tokens (debug)")
        # Display tokens list or string
        tokens = result.get('output_tokens', [])
        st.write(tokens)

        # Prepare combined download (resume + metadata)
        zip_buffer = io.BytesIO()
        with ZipFile(zip_buffer, "w") as zip_file:
            # Add generated resume docx
            zip_file.writestr("redrafted_resume.docx", result['resume_docx'].getvalue())
            # Add metadata JSON
            metadata = {
                'facts': result.get('facts_json'),
                'tokens': result.get('output_tokens')
            }
            zip_file.writestr("metadata.json", json.dumps(metadata, indent=2))
        zip_buffer.seek(0)

        st.download_button(
            label="Download Results",
            data=zip_buffer,
            file_name="results.zip",
            mime="application/zip"
        )
