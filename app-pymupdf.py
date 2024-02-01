import streamlit as st
import fitz  # PyMuPDF
from io import BytesIO

def pdf_to_text(file_content):
    doc = fitz.open(stream=BytesIO(file_content), filetype="pdf")
    text = ""
    
    for page_number in range(doc.page_count):
        page = doc.load_page(page_number)
        text += str(page.get_text())
    
    doc.close()
    return text

# Streamlit UI
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Use BytesIO to read the content of the uploaded file
    file_content = uploaded_file.read()
    
    # Pass the BytesIO content to the pdf_to_text function
    text_result = pdf_to_text(file_content)
    
    # Display the extracted text
    st.text(text_result)
