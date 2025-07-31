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
