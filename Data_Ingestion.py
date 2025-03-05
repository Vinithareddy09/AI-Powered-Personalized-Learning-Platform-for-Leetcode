import PyPDF2
import docx
import sys
import logging

def load_data(doc):
    """
    Loads and preprocesses the document.
    """
    if doc.name.endswith('.pdf'):
        return load_pdf(doc)
    elif doc.name.endswith('.docx'):
        return load_docx(doc)
    else:
        raise ValueError("Unsupported file format")

def load_pdf(pdf_file):
    reader = PyPDF2.PdfFileReader(pdf_file)
    text = ""
    for page_num in range(reader.numPages):
        page = reader.getPage(page_num)
        text += page.extract_text()
    return text

def load_docx(docx_file):
    doc = docx.Document(docx_file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text
    return text
