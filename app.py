import openai
import PyPDF2
import streamlit as st

# Set up OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your OpenAI API key

# Function to read PDF and extract text
def read_pdf(file_path):
    pdf_text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            pdf_text += page.extract_text()
    return pdf_text

# Function to query GPT-3.5 Turbo
def query_gpt_turbo(question, context):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{question}\n\n{context}"}
        ],
        max_tokens=4096,
        temperature=0.5
    )
    return response.choices[0].message['content']

# Streamlit app
st.title("BOUSST AI PORTAL")
question = st.text_input("Enter your question")

# Read the PDF
pdf_file_path = 'cse.pdf'  # Ensure you have the PDF file in your project directory
pdf_text = read_pdf(pdf_file_path)

if question:
    with st.spinner("Searching..."):
        answer = query_gpt_turbo(question, pdf_text)
        st.write(answer)

if not question:
    st.info("Please enter a question to get started.")

