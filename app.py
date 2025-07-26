import json
import streamlit as st
from utils import parse_resume_file, extract_facts
from chains.resume_rewrite_chain import get_resume_rewrite_chain

st.set_page_config(page_title="AI RAG Resume Rewriter", layout="wide")

def main():
    st.title("AI‑Powered Resume Rewrite")

    # 1️⃣ Upload & parse resume
    uploaded = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
    if not uploaded:
        st.info("Please upload a resume to start.")
        return
    resume_text = parse_resume_file(uploaded)

    # 2️⃣ Paste job description
    job_desc = st.text_area("Paste Target Job Description", height=200)
    if not job_desc:
        st.info("Enter the job description to tailor your resume.")
        return

    # 3️⃣ Extract facts
    facts_json = extract_facts(resume_text)

    # 4️⃣ LLM parameters
    col1, col2 = st.columns(2)
    with col1:
        temp = st.slider("Generation Temperature", 0.0, 1.0, 0.7, 0.05)
    with col2:
        max_toks = st.number_input("Max Output Tokens", min_value=100, max_value=2000, value=800)

    # 5️⃣ Run rewrite
    if st.button("Rewrite Resume"):
        chain = get_resume_rewrite_chain(temperature=temp, max_tokens=max_toks)
        with st.spinner("Rewriting…"):
            result_obj = chain.invoke({
                "resume": resume_text,
                "job_description": job_desc,
                "facts_json": facts_json
            })

        rewritten = result_obj.generations[0][0].text
        usage = result_obj.llm_output["token_usage"]

        # 6️⃣ Display
        st.subheader("Rewritten Resume")
        st.text_area("", value=rewritten, height=300)

        # 7️⃣ Downloads
        st.download_button(
            "Download Prompt Tokens",
            data=json.dumps({"prompt_tokens": usage["prompt_tokens"]}, indent=2),
            file_name="input_tokens.json",
            mime="application/json",
        )
        st.download_button(
            "Download Total Tokens",
            data=json.dumps({"total_tokens": usage["total_tokens"]}, indent=2),
            file_name="total_tokens.json",
            mime="application/json",
        )
        st.download_button(
            "Download Output Tokens",
            data=json.dumps({"completion_tokens": usage["completion_tokens"]}, indent=2),
            file_name="output_tokens.json",
            mime="application/json",
        )

if __name__ == "__main__":
    main()
