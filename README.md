# AI-Powered Resume Analyzer
An intelligent web application that provides instant, data-driven feedback on resumes. Users can upload their resume (PDF or DOCX) and receive a comprehensive analysis of its structure, content, and ATS-friendliness, powered by the Google Gemini API.



#  ✨ Key Features
File Upload: Securely upload resumes in PDF or DOCX format.

AI-Powered Analysis: Leverages the Google Gemini API to generate an in-depth "Resume Report Card."

Grading System: Provides an overall letter grade (e.g., A+, B-, C) for a quick, actionable assessment.

Detailed Feedback: Breaks down the analysis into graded sections like "Content & Language" and "Formatting & Structure."

Resume Improvement: Includes a feature to automatically rewrite and enhance the resume text using AI.

Modern UI: A clean, professional, and responsive user interface built with Flask and Tailwind CSS.

# 🛠️ Technology Stack
# Backend:

Python 3

Flask: A lightweight web framework for the server and API.

Google Gemini API (google-generativeai): The core AI model for analysis and text generation.

PyMuPDF (fitz): For extracting text from PDF files.

python-docx: For extracting text from DOCX (Microsoft Word) files.

# Frontend:

HTML5

Tailwind CSS: For modern, utility-first styling.

Vanilla JavaScript: For handling file uploads and dynamic UI updates via Fetch API.

# 🚀 Getting Started
To get a local copy up and running, follow these simple steps.

Prerequisites
Python 3.8+

An active Google Gemini API Key.

Installation & Setup
Clone the repository:

git clone [https://github.com/YOUR_USERNAME/AI-Resume-Analyzer.git](https://github.com/YOUR_USERNAME/AI-Resume-Analyzer.git)
cd AI-Resume-Analyzer

Create and activate a virtual environment:

# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python -m venv venv
source venv/bin/activate

Install the required packages:

pip install -r requirements.txt

Configure your environment variables:

Create a new file named .env in the root of the project.

Open the .env.example file, copy its content, and paste it into your new .env file.

Replace PASTE_YOUR_API_KEY_HERE with your actual Google Gemini API key.

GEMINI_API_KEY="YOUR_SECRET_API_KEY"

# Running the Application
Start the Flask server:

flask run
