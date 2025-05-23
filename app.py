from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import os
import fitz  # PyMuPDF
import re

app = Flask(__name__)
CORS(app)

# Gemini API key
GEMINI_API_KEY = os.environ.get("token_gemini")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set")

GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# Fixed URLs to scrape
FIXED_URLS = [
    "https://www.bou.ac.bd/",
    "https://bousst.edu.bd/"
]

# Extract text from PDF
def extract_pdf_text(pdf_path="cse.pdf", max_chars=3000):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text[:max_chars].strip()
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

# Scrape websites
def scrape_sites():
    all_text = ""
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    for url in FIXED_URLS:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text(separator=' ')
            all_text += text + "\n\n"
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    return all_text[:3000]

# Ask Gemini
def ask_gemini(context, question):
    try:
        prompt = f"You are an agent of BOUSST Info Center. Use the following information to answer:\n\n{context}\n\nQuestion: {question}"
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }
        response = requests.post(
            GEMINI_ENDPOINT,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=15
        )
        response.raise_for_status()
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text'].strip()

    except Exception as e:
        return f"Gemini API error: {str(e)}"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"answer": "Please provide a question."})

    pdf_context = extract_pdf_text()
    web_context = scrape_sites()

    # Combine both PDF and web context
    full_context = f"{pdf_context}\n\n{web_context}"
    answer = ask_gemini(full_context, question)
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)
