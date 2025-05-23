from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)
CORS(app)

# Gemini API key
GEMINI_API_KEY = "token_gemini"  # Replace with your real API key
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set")

GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

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
    return all_text[:3000]  # limit to 3000 chars

def ask_gemini(context, question):
    try:
        prompt = f"Context: {context}\n\nQuestion: {question}"
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

    context = scrape_sites()
    answer = ask_gemini(context, question)
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)
