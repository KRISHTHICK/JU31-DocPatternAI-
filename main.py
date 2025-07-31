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
