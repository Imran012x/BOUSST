import os
import requests
import PyPDF2
import json  # Added import statement for json
from flask import Flask, request, jsonify

app = Flask(__name__)

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

# Save PDF text for future access
pdf_text = extract_pdf_text(PDF_FILE_PATH)

# Function to query Google Gemini
def query_gemini(query):
    combined_query = (
        f"Here is the text from the PDF: {pdf_text}\n\n"
        f"User Query: {query}\n"
        "Please analyze the PDF text and provide an answer based on the content.When You will answer as like you are the head of the info center of bou(bangladesh open university,so donot give any initial talk like the pdf has this or that.Direct talk as like you are answering face to face ."
    )
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"
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
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
        result = response.json()
        print("Full API response:", json.dumps(result, indent=2))
        return result
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Root endpoint
@app.route('/')
def index():
    return "Welcome to the Project"

# Flask API endpoint
@app.route('/ask', methods=['POST'])
def ask_question():
    query = request.json.get("query")

    # Check if the query is found in the PDF text
    #if query in pdf_text:
        #answer = f"Found in PDF: The information related to your query '{query}' is available in the document."
    #else:
    answer = query_gemini(query)  # Get answer from Gemini using the query

    # Optionally save the answer for future requests
    save_answer(query, answer)

    return jsonify({"answer": answer})

def save_answer(query, answer):
    # Implement logic to save the answer to a database or file for future retrieval
    pass

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Get the port from environment variable or use 5000
    app.run(host='0.0.0.0', port=port)
