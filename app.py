from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import os
import openai

app = Flask(__name__)
CORS(app)

# OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set")

openai.api_key = OPENAI_API_KEY

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

def ask_openai(context, question):
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant that answers questions based on the given context."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=300,
            temperature=0.7,
        )

        answer = response.choices[0].message.content.strip()
        return answer

    except Exception as e:
        return f"OpenAI API error: {str(e)}"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"answer": "Please provide a question."})

    context = scrape_sites()
    answer = ask_openai(context, question)
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)











# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import requests
# from bs4 import BeautifulSoup
# import os

# app = Flask(__name__)
# CORS(app)

# # Hugging Face API setup
# HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/deepseek-ai/deepseek-llm-7b-chat"
# HUGGINGFACE_TOKEN = os.getenv("token_hf")

# if not HUGGINGFACE_TOKEN:
#     raise ValueError("HUGGINGFACE_TOKEN environment variable not set")

# HEADERS = {
#     "Authorization": f"Bearer {HUGGINGFACE_TOKEN}"
# }

# # Fixed URLs to scrape
# FIXED_URLS = [
#     "https://www.bou.ac.bd/",
#     "https://bousst.edu.bd/"
# ]

# # Scrape and extract text from the target websites
# def scrape_sites():
#     all_text = ""
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/91.0 Safari/537.36"
#     }

#     for url in FIXED_URLS:
#         try:
#             response = requests.get(url, headers=headers, timeout=10)
#             soup = BeautifulSoup(response.text, 'html.parser')
#             text = soup.get_text(separator=' ')
#             all_text += text + "\n\n"
#         except Exception as e:
#             print(f"Error scraping {url}: {e}")

#     return all_text[:3000]  # Limit to 3000 characters for performance

# # Send context + question to Hugging Face API
# def ask_deepseek(context, question):
#     payload = {
#         "inputs": f"Context: {context}\n\nQuestion: {question}",
#         "parameters": {"max_new_tokens": 300}
#     }

#     try:
#         res = requests.post(HUGGINGFACE_API_URL, headers=HEADERS, json=payload)
#         result = res.json()
#         print("Hugging Face response:", result)

#         if isinstance(result, list) and "generated_text" in result[0]:
#             return result[0]["generated_text"].split("Question:")[-1].strip()
#         else:
#             return f"DeepSeek error: {result.get('error', 'Unknown error')}"
#     except Exception as e:
#         return f"Error contacting DeepSeek API: {e}"

# # API endpoint
# @app.route("/ask", methods=["POST"])
# def ask():
#     data = request.get_json()
#     question = data.get("question", "").strip()

#     if not question:
#         return jsonify({"answer": "Please provide a question."})

#     context = scrape_sites()
#     answer = ask_deepseek(context, question)
#     return jsonify({"answer": answer})

# if __name__ == '__main__':
#     app.run(debug=True)
