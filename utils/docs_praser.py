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
