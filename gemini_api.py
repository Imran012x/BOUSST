import os
import requests
import PyPDF2
import json

# Constants
GEMINI_API_KEY = os.environ.get("MY_GEMINI_API_KEY")  # Securely use the environment variable
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"  # API URL
PDF_FILE_PATH = "cse.pdf"  # Update with your PDF path

# Extract text from PDF
def extract_pdf_text(file_path):
    pdf_text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            pdf_text += page.extract_text() or ""  # Ensure we don't add None if extract_text() fails
    return pdf_text

# Load PDF text for future use
pdf_text = extract_pdf_text(PDF_FILE_PATH)

# Function to query Google Gemini
def query_gemini(query):
    combined_query = (
        f"Here is the text from the PDF: {pdf_text}\n\n"
        f"User Query: {query}\n"
        "Please analyze the PDF text and provide an answer based on the content. Respond as though you are the head of the info center at Bangladesh Open University, answering directly."
    )
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": combined_query
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(GEMINI_API_URL, json=data, headers=headers, params={"key": GEMINI_API_KEY})
        response.raise_for_status()  # Check for HTTP errors
        result = response.json()
        print("Full API response:", json.dumps(result, indent=2))
        return result
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
