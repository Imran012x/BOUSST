from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)
CORS(app)

# Replace with your Hugging Face token (free to create)
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/deepseek-ai/deepseek-llm-7b-chat"
# HUGGINGFACE_TOKEN = "token_hf"
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")


HEADERS = {
    "Authorization": f"Bearer {HUGGINGFACE_TOKEN}"
}

FIXED_URLS = [
    "https://www.bou.ac.bd/",
    "https://bousst.edu.bd/"
]

def scrape_sites():
    all_text = ""
    for url in FIXED_URLS:
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text(separator=' ')
            all_text += text + "\n\n"
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    return all_text[:3000]  # Limit to 3000 chars

def ask_deepseek(context, question):
    payload = {
        "inputs": f"Context: {context}\n\nQuestion: {question}",
        "parameters": {"max_new_tokens": 300}
    }
    res = requests.post(HUGGINGFACE_API_URL, headers=HEADERS, json=payload)
    result = res.json()
    if isinstance(result, list):
        return result[0]["generated_text"].split("Question:")[-1].strip()
    else:
        return "DeepSeek error or rate limit."

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    context = scrape_sites()
    answer = ask_deepseek(context, question)
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)
