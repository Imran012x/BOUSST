import openai
import PyPDF2
import streamlit as st
import os
#from dotenv import load_dotenv

# Load environment variables from .env file
#load_dotenv()

# Setup OpenAI API Key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to read PDF and extract text
def read_pdf(file_path):
    pdf_text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            pdf_text += page.extract_text()
    return pdf_text

# Function to query GPT with the new API (Version 1.0.0 and above)
def query_gpt_turbo(question, context):
    # Call the OpenAI API to get a response from GPT
    response = openai.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{question}\n\n{context}"}
        ],
        max_tokens=4096,
        temperature=0.5
    )
    return response['choices'][0]['message']['content']

# Streamlit app
st.markdown("<h1 style='text-align: center;'>BOUSST AI PORTAL</h1>", unsafe_allow_html=True)

# Ask for a question
question = st.text_input("Enter your question")

# PDF file path (set the path to your PDF file)
pdf_file_path = 'cse.pdf'
pdf_text = read_pdf(pdf_file_path)

# Automatically provide the answer when the user presses Enter
if question:
    with st.spinner("Searching..."):
        start = 0
        answer_found = False
        while start < len(pdf_text):
            chunk = pdf_text[start:start + 4000]
            answer = query_gpt_turbo(question, chunk)

            if "not available" not in answer.lower():
                st.write(answer)
                answer_found = True
                break

            start += 4000

        if not answer_found:
            st.write("Sorry, I couldn't find that in the PDF. Here is a general answer to your question.")

if not question:
    st.info("Please enter a question to get started.")
