from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import io
import base64   # FIX ✅
from PIL import Image
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=os.getenv("API_KEY"))

def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([
        {"role": "user", "parts": [
            {"text": input_text},
            pdf_content[0],   # first page image
            {"text": prompt}
        ]}
    ])
    return response.text

# def input_pdf_setup(uploaded_file):
#     if uploaded_file is not None:
#         # Convert PDF to images (requires Poppler installed)
#         images = pdf2image.convert_from_bytes(
#             uploaded_file.read(),
#             poppler_path=r"C://poppler//poppler-25.07.0//Library//bin"   # update this path ✅
#         )
#         first_page = images[0]
#         img_byte_arr = io.BytesIO()
#         first_page.save(img_byte_arr, format='JPEG')
#         img_byte_arr = img_byte_arr.getvalue()

#         pdf_parts = [
#             {
#                 "mime_type": "image/jpeg",
#                 "data": base64.b64encode(img_byte_arr).decode()
#             }
#         ]
#         return pdf_parts
#     else:
#         raise FileNotFoundError("No file uploaded")
import fitz  # PyMuPDF
import base64
import io

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        pdf_data = uploaded_file.read()
        doc = fitz.open(stream=pdf_data, filetype="pdf")
        first_page = doc.load_page(0)
        pix = first_page.get_pixmap()
        img_byte_arr = pix.tobytes("jpg")

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit UI
st.set_page_config(page_title="ATS Resume Scorer", page_icon=":guardsman:", layout="wide")
st.header("ATS Resume Scorer :guardsman:")

input_text = st.text_area("Enter Job Description: ", key="input_text")
uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])
if uploaded_file is not None:
    st.write("Uploaded Resume:")

submit1 = st.button("Tell me about the resume")   # fixed typo ✅
submit2 = st.button("How can I Improve my skills")
submit3 = st.button("Percent match with job description")

input_prompt1 = """
You are an experienced HR with tech experience in the field of data science, 
full stack web development, big data engineering, devops, data analyst. 
Your task is to review the resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate’s profile 
highlights the strengths and weaknesses of the applicant in relation to the job description.
give bullet points with just headings.
"""
input_prompt2 = """
How can I improve my skills to get a job according to the resume?
give bullet points with just headings.
"""
input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding 
of data science, full stack web development, big data engineering, devops, data analyst, 
and ATS functionality. Your task is to compare the resume against the job description 
and provide a percentage match score based on the relevance of skills, experience, and qualifications.
The output should come as percentage.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload a resume to proceed.")
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload a resume to proceed.")
elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload a resume to proceed.")
