from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import gemini  # Import the gemini module for querying

load_dotenv()

app = Flask(__name__)

@app.route('/ask', methods=['GET'])
def ask_question():
    try:
        data = request.json  # Get the JSON data from the request
        query = data['contents'][0]['parts'][0]['text']
        result = gemini.query_gemini(query)  # Use the query_gemini function from gemini.py
        return jsonify(result)
    except KeyError as e:
        return jsonify({"error": f"Missing key: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port,debug=True)
