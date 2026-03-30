from docx import Document

def load_base_resume(path):
    doc = Document(path)
    text = "\n".join([p.text for p in doc.paragraphs])
    return text