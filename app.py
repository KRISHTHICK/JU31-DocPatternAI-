import streamlit as st
from utils.doc_parser import load_document, get_sections
from utils.table_detector import extract_tables_from_doc
from utils.pattern_learner import learn_table_patterns, save_patterns
import json

st.title("📄 DocPatternAI - AI Structure Learner")

uploaded = st.file_uploader("Upload MS Word Document (.docx)", type="docx")

if uploaded:
    doc = load_document(uploaded)
    st.success("Document loaded.")

    sections = get_sections(doc)
    tables = extract_tables_from_doc(doc)
    patterns = learn_table_patterns(tables)

    st.subheader("📘 Detected Sections")
    for sec in sections:
        st.markdown(f"### {sec['heading']}")

    st.subheader("📊 Table Pattern Summary")
    st.json(patterns)

    if st.button("💾 Save Pattern JSON"):
        save_patterns(patterns)
        st.success("Patterns saved.")
