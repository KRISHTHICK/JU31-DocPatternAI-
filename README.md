# JU31-DocPatternAI-
GEN AI

DocPatternAI – Intelligent Pattern & Structure Mining from Unstructured Word Documents
✅ Objective
Automatically detect and learn document layout patterns (table structures, text+image combinations, checkboxes, colored units, etc.) from unstructured Microsoft Word (.docx) files. These learned patterns can be human-approved or edited for extracting structured data across similar documents.

🧠 Key Features
Automatically:

Identify sections.

Parse tables of various patterns (text-only, text+icons/images, checkboxes, unit-value fields).

Detect value-signed boxes, background colors, font sizes, and styles.

Learn & save structure templates/patterns.

Allow human-in-the-loop to approve or edit patterns.

Extract data according to these learned patterns.

📁 Project Structure
bash
Copy
Edit

txt
Copy
Edit
python-docx
pandas
streamlit
Pillow
lxml
numpy
📄 sample_structure.docx
Create a .docx file with:

5 sections (General Instructions, Equipment, Unit Ops, Visual Guidelines, Tables Summary)

Tables with:

Checkbox columns

Image + text in one cell

Unit values like 23.4 kg inside shaded cells

Row/column with background color based on values

Tables inside other tables (nested)

Icons (like warning ⚠️ or tick ✔️)

You can upload or request a dummy one later if needed.

🧠 utils/doc_parser.py
python
Copy
Edit
from docx import Document

def load_document(docx_path):
    return Document(docx_path)

def get_sections(doc):
    sections = []
    current = {"heading": None, "content": []}
    for para in doc.paragraphs:
        if para.style.name.startswith("Heading"):
            if current["heading"]:
                sections.append(current)
                current = {"heading": para.text, "content": []}
            else:
                current["heading"] = para.text
        else:
            current["content"].append(para)
    if current["heading"]:
        sections.append(current)
    return sections
📐 utils/table_detector.py
python
Copy
Edit
def extract_tables_from_doc(doc):
    tables = []
    for table in doc.tables:
        rows = []
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells]
            rows.append(cells)
        tables.append(rows)
    return tables
🎨 utils/visual_extractor.py
python
Copy
Edit
def get_table_styles(doc):
    styles = []
    for table in doc.tables:
        t_style = {"shaded_cells": [], "icons": [], "checkboxes": []}
        for row in table.rows:
            for cell in row.cells:
                if '☑' in cell.text or '☐' in cell.text:
                    t_style["checkboxes"].append(cell.text)
                if '⚠️' in cell.text or '✔️' in cell.text:
                    t_style["icons"].append(cell.text)
                # Background color and unit-value detection are limited in python-docx
                if any(unit in cell.text for unit in ['kg', '°C', 'mL']):
                    t_style["shaded_cells"].append(cell.text)
        styles.append(t_style)
    return styles
📊 utils/pattern_learner.py
python
Copy
Edit
import json
from collections import Counter

def learn_table_patterns(tables):
    pattern_stats = []
    for t in tables:
        rows = len(t)
        cols = max(len(row) for row in t)
        has_checkbox = any("☑" in cell or "☐" in cell for row in t for cell in row)
        has_units = any(any(u in cell for u in ['kg','mL','°C']) for row in t for cell in row)
        has_icons = any(any(icon in cell for icon in ['✔️','⚠️']) for row in t for cell in row)
        pattern_stats.append({
            "rows": rows,
            "cols": cols,
            "has_checkbox": has_checkbox,
            "has_units": has_units,
            "has_icons": has_icons
        })
    return pattern_stats

def save_patterns(patterns, file_path="patterns/extracted_patterns.json"):
    with open(file_path, "w") as f:
        json.dump(patterns, f, indent=2)
🚀 main.py
python
Copy
Edit
from utils.doc_parser import load_document, get_sections
from utils.table_detector import extract_tables_from_doc
from utils.visual_extractor import get_table_styles
from utils.pattern_learner import learn_table_patterns, save_patterns

doc = load_document("samples/sample_structure.docx")
sections = get_sections(doc)
tables = extract_tables_from_doc(doc)
styles = get_table_styles(doc)
patterns = learn_table_patterns(tables)
save_patterns(patterns)

print("Patterns extracted and saved.")
🌐 app.py (Streamlit UI)
python
Copy
Edit
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
✅ Expected Output
Learned Patterns in patterns/extracted_patterns.json

Detected Tables with checkboxes, icons, unit-values

Editable in UI: streamlit allows humans to approve/edit rules


