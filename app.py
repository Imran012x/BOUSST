from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF

app = Flask(__name__)
CORS(app)

# Gemini API key
GEMINI_API_KEY = os.environ.get("token_gemini")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set")

GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# Function to extract text from PDF
def extract_pdf_text(pdf_path="cse.pdf"):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        # Remove excessive whitespace and clean the text
        text = " ".join(text.split())
        # Note: Gemini API has a token limit (e.g., ~1M tokens for Gemini 2.0 Flash).
        # If text is too long, you may need to truncate or chunk it.
        # For now, send full text unless API limit is hit.
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

# (Commented) Web scraping logic
"""
# Fixed URLs to scrape
FIXED_URLS = [
    "https://www.bou.ac.bd/",
    "https://bousst.edu.bd/"
]

def scrape_sites():
    all_text = ""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/91.0 Safari/537.36"
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
"""

# Ask Gemini with PDF context
def ask_gemini(context, question):
    try:
        prompt = (
            f"You are a professional and knowledgeable agent from the BOUSST Info Center. "
            f"Your role is to provide accurate, clear, and helpful answers to users' questions about BOUSST, "
            f"acting as if you are directly representing the institution. Do not mention or reference any specific documents, PDFs, or sources in your response. "
            f"Instead, answer conversationally and authoritatively as if you have direct access to all relevant BOUSST information. "
            f"If you cannot find the answer to the question in the provided information, respond with: 'I am sorry, I cannot provide the info right now.' "
            f"Use a friendly and professional tone, and avoid technical jargon unless necessary.\n\n"
            f"Context (for your reference only, do not mention in response):\n{context}\n\n"
            f"Question: {question}"
        )

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

    context = extract_pdf_text()
    # Optionally add scraped content: context += scrape_sites()
    answer = ask_gemini(context, question)
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)
