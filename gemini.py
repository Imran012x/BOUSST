import requests
import os
import PyPDF2

# Constants
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
GEMINI_API_KEY = os.getenv("MY_GEMINI_API_KEY")  # Get the API key from environment variable
PDF_FILE_PATH = "/home/imran/Documents/Drive/BOUSST-main/cse.pdf"  # Update this with the actual PDF file path

# Extract text from PDF
def extract_pdf_text(file_path):
    pdf_text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            pdf_text += page.extract_text() or ""  # Ensure we don't add None if extract_text() fails
    return pdf_text

# Load PDF text for future use
pdf_text = extract_pdf_text(PDF_FILE_PATH)

# Function to query Google Gemini
def query_gemini(query):
    combined_query = (
        f"Here is the text from the PDF: {pdf_text}\n\n"
        f"User Query: {query}\n"
        "Please analyze the PDF text and provide an answer based on the content. Respond as though you are the head of the info center at Bangladesh Open University, answering directly without initial any text."
    )

    # Create the payload for the Gemini API
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": combined_query  # Send the combined query including PDF text
                    }
                ]
            }
        ]
    }

    # Send the request to the Gemini API
    response = requests.post(GEMINI_API_URL, json=payload, params={"key": GEMINI_API_KEY})
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()  # Return the response from Gemini API as JSON
