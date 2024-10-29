import os
import requests
import PyPDF2
from flask import Flask, request, jsonify

app = Flask(__name__)

# Constants
GEMINI_API_KEY = os.environ.get("MY_GEMINI_API_KEY")  # Securely use the environment variable
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=" + GEMINI_API_KEY
PDF_FILE_PATH = "cse.pdf"  # Update with your PDF path

# Extract text from PDF
def extract_pdf_text(file_path):
    pdf_text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()
    return pdf_text

# Save PDF text for future access
pdf_text = extract_pdf_text(PDF_FILE_PATH)

# Function to query Google Gemini
def query_gemini(query):
    payload = {
        "contents": [{"parts": [{"text": query}]}]
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(GEMINI_API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("answer")
    else:
        return f"Error: {response.status_code}, {response.text}"

# Flask API endpoint
@app.route('/ask', methods=['POST'])
def ask_question():
    query = request.json.get("query")
    
    # Check if the query is related to the PDF text
    if query in pdf_text:
        answer = query_gemini(query)  # Get answer from Gemini using the query
    else:
        answer = "I'm sorry, but I couldn't find the information you requested in the document."

    # Save the answer for future requests (optional, depending on your use case)
    save_answer(query, answer)
    
    return jsonify({"answer": answer})

def save_answer(query, answer):
    # Implement logic to save the answer to a database or file for future retrieval
    pass

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Get the port from environment variable or use 5000
    app.run(host='0.0.0.0', port=port)
