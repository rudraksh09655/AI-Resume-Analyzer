import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import fitz  # PyMuPDF for PDFs
import docx  # python-docx for Word docs

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for the app

# --- AI Model Configuration ---
try:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key or api_key == "PASTE_YOUR_API_KEY_HERE":
        raise ValueError("API Key not found. Please set a valid GEMINI_API_KEY in your .env file.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
except Exception as e:
    # If the model fails to configure, print a fatal error and exit.
    print(f"FATAL ERROR: Could not configure the AI model: {e}")
    exit()


# --- Helper Function to Extract Text from Files ---
def extract_text_from_file(file):
    """Extracts text from uploaded PDF, DOCX, or TXT files."""
    filename = file.filename
    try:
        if filename.endswith('.pdf'):
            doc = fitz.open(stream=file.read(), filetype="pdf")
            text = "".join(page.get_text() for page in doc)
            return text
        elif filename.endswith('.docx'):
            doc = docx.Document(file)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
        elif filename.endswith('.txt'):
            return file.read().decode('utf-8')
        else:
            return None  # Unsupported file type
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        return None


# --- NEW, CORRECTED REQUEST VALIDATION LOGIC ---
def validate_and_extract_text(request):
    """
    Validates the incoming request and extracts text from the file.
    Returns a tuple: (text, error_response).
    On success, error_response will be None.
    On failure, text will be None.
    """
    if 'resume_file' not in request.files:
        return None, jsonify({"error": "No resume file found in the request"}), 400

    file = request.files['resume_file']
    if file.filename == '':
        return None, jsonify({"error": "No file selected"}), 400

    resume_text = extract_text_from_file(file)
    if resume_text is None:
        return None, jsonify(
            {"error": "Unsupported file type or error reading file. Please use PDF, DOCX, or TXT."}), 400

    if not resume_text.strip():
        return None, jsonify({"error": "The uploaded file appears to be empty."}), 400

    # If all checks pass, return the text and no error
    return resume_text, None, None


# --- Flask Routes (API Endpoints) ---

@app.route("/")
def index():
    """Serves the main HTML page."""
    return render_template("index.html")


@app.route('/analyze', methods=['POST'])
def analyze_resume():
    """Analyzes the uploaded resume and returns a graded report."""
    resume_text, error_response, status_code = validate_and_extract_text(request)
    if error_response:
        return error_response, status_code

    prompt = f"""
        Act as a strict but fair university career counselor grading a resume.
        Your entire response MUST follow this format exactly, with no extra commentary before or after.

        First, provide an overall letter grade on a single line, like this:
        Overall Grade: [A, B+, C-, etc.]

        Next, provide a detailed report with grades for each of the following three sections. Use the exact titles and formatting:

        ### Content & Language: [Grade]
        * Provide at least two bullet points analyzing action verbs, clarity, and impact.

        ### Formatting & Structure: [Grade]
        * Provide at least two bullet points on layout, readability, and use of white space.

        ### Keyword Relevance: [Grade]
        * Provide at least two bullet points on ATS optimization and industry-specific terminology.

        Resume to Grade:
        ---
        {resume_text}
    """
    try:
        response = model.generate_content(prompt)
        return jsonify({"feedback": response.text})
    except Exception as e:
        print(f"AI Model Error: {e}")
        return jsonify({"error": "Failed to get analysis from the AI model."}), 500


@app.route('/improve', methods=['POST'])
def improve_resume():
    """Improves the uploaded resume text."""
    resume_text, error_response, status_code = validate_and_extract_text(request)
    if error_response:
        return error_response, status_code

    prompt = f"""
        Act as a professional resume writer. Rewrite and improve the following resume text.
        Make it more professional, concise, and optimized for ATS. Use strong action verbs.
        Return ONLY the improved resume text, without any additional commentary.

        Original Resume Text:
        ---
        {resume_text}
    """
    try:
        response = model.generate_content(prompt)
        return jsonify({"improved_resume": response.text})
    except Exception as e:
        print(f"AI Model Error: {e}")
        return jsonify({"error": "Failed to get improvement from the AI model."}), 500


# --- Start the Flask App ---
if __name__ == '__main__':
    app.run(debug=True)

