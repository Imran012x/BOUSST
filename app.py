from flask import Flask, request, jsonify
from gemini_api import query_gemini  # Import the query function

app = Flask(__name__)

# Root endpoint
@app.route('/')
def index():
    return "Welcome to the Project"

# Flask API endpoint for asking questions
@app.route('/ask', methods=['POST'])
def ask_question():
    query = request.json.get("query")
    answer = query_gemini(query)  # Call the Gemini API through the query function
    return jsonify({"answer": answer})

# Ensure the app runs only when called directly
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))  # Get the port from environment variable or use 5000
    app.run(host='0.0.0.0', port=port)
