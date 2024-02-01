from dotenv import load_dotenv
load_dotenv()  # Read variables from .env

import os
import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

# import PyPDF2 as pdf
# def pdf_to_text(file):
#     reader = pdf.PdfReader(file)
#     text = ""
#     for page in reader(len(reader.pages)):
#         page = reader.pages[page]
#         text += str(page.extract_text())
#     return text

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

# Prompt Template
input_prompt = """
Hello, assuming you are an experienced ATS (Application Tracking System)
with an in depth understanding of software engineering, technologies, 
data science, data analyst and/or data engineer. 
Please evaluate the uploaded resume based on the given job description.
You must consider the competitive job market and provide the best assistance
for improving the users' resumes. Assign the percentage Matching based 
on the job description and the missing keywords with a good accuracy.
Resume:{text}
Job Description:{job_description}

Generate the response in a single string with the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

# Initialize the streamlit app
import streamlit as st

st.set_page_config(page_title="Gemini Pro - Resume & Job Description Matching")
st.header("Gemini Pro - Resume & Job Description Matching")

# Sidebar content
with st.sidebar:  
    st.markdown('''
        ## About
        This app is Gemini-powered resume & job description matching system, built using:
        - [Streamlit](https://streamlit.io/)
        - [Gemini Pro](https://cloud.google.com/vertex-ai/docs/generative-ai/multimodal/overview) LLM Model
        ''')
    st.write("Made with ❤️ by Amzad Basha.")

# UI Content        
job_description = st.text_area("Enter the Job Description")
uploaded_file = st.file_uploader("Upload the resume in PDF format", type="pdf")

submit = st.button("Submit")

# When the button is clicked
if submit: 
    # Use BytesIO to read the content of the uploaded file
    file_content = uploaded_file.read()
    
    # Pass the BytesIO content to the pdf_to_text function
    text_result = pdf_to_text(file_content)
    
    response = get_response(input_prompt)
    st.subheader("The Response is")
    st.write(response)