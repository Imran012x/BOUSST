import requests
import PyPDF2
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Constants
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"  # Use a secure method for handling API keys
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=GEMINI_API_KEY"
PDF_FILE_PATH = "cse.pdf"  # Update with your PDF path
BOU_URL = "https://www.bou.ac.bd"

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
def query_gemini(query, pdf_text=None):
    payload = {
        "query": query,
        "context": pdf_text
    }
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(GEMINI_API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("answer")
    else:
        return f"Error: {response.status_code}, {response.text}"

# Web scrape function
def scrape_bou_website(query):
    response = requests.get(BOU_URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.find_all(string=lambda text: query.lower() in text.lower())
        return results[0] if results else "No relevant information found on the BOU website."
    else:
        return "Failed to access BOU website."

# Flask API endpoint
@app.route('/ask', methods=['POST'])
def ask_question():
    query = request.json.get("query")
    answer = answer_question(query)
    return jsonify({"answer": answer})

# Main function to handle the question
def answer_question(query):
    answer = query_gemini(query, pdf_text)
    
    if "No answer found" in answer:
        bou_answer = scrape_bou_website(query)
        if bou_answer != "No relevant information found on the BOU website.":
            return bou_answer
        else:
            return query_gemini(query)
    return answer

if __name__ == '__main__':
    app.run(debug=True)

