from flask import Flask, request, render_template, jsonify, send_from_directory
import pdfplumber
import re
import spacy
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config.update({
    'UPLOAD_FOLDER': 'uploads/',
    'OUTPUT_FOLDER': 'output/',
    'MAX_CONTENT_LENGTH': 5 * 1024 * 1024,  # 5MB file size limit
    'ALLOWED_EXTENSIONS': {'pdf'}
})

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Load NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    raise RuntimeError("Please install the English language model:\n"
                      "python -m spacy download en_core_web_sm")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_entities(text):
    """Extract structured information from resume text"""
    # Personal Information
    emails = list(set(re.findall(r'[\w\.-]+@[\w\.-]+', text)))
    phones = list(set(re.findall(r'(\+?\d{1,3}[-\.\s]?)?\(?\d{3}\)?[-\.\s]?\d{3}[-\.\s]?\d{4}', text)))
    
    # Social Links
    github_links = list(set(re.findall(r'github\.com/[a-zA-Z0-9-]+', text)))
    linkedin_links = list(set(re.findall(r'linkedin\.com/in/[a-zA-Z0-9-]+', text)))
    
    # Education
    education = re.findall(r'(Education|Academic Background)[\s\S]*?(?=(Experience|Skills|\Z))', text, re.IGNORECASE)
    
    # Experience
    experience_years = re.findall(r'(\d+)\s*(years?|yrs?)\s*(experience|of experience)', text, re.IGNORECASE)
    
    # Skills
    skills_list = {
        "Technical": ["Python", "SQL", "Machine Learning", "Pandas", "Numpy"],
        "Tools": ["Excel", "Power BI", "Tableau", "Jupyter"],
        "Soft Skills": ["Communication", "Teamwork", "Leadership"]
    }
    
    found_skills = {category: [] for category in skills_list}
    for category, skills in skills_list.items():
        for skill in skills:
            if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
                found_skills[category].append(skill)
    
    return {
        "personal_info": {
            "emails": emails,
            "phones": phones
        },
        "social_links": {
            "github": github_links,
            "linkedin": linkedin_links
        },
        "education": education[0][0] if education else None,
        "experience": f"{experience_years[0][0]} years" if experience_years else "Not specified",
        "skills": found_skills,
        "extraction_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.route('/')
def home():
    """Render main page"""
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Template rendering failed: {str(e)}", 500

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and processing"""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400
    
    if not (file and allowed_file(file.filename)):
        return jsonify({"error": "Only PDF files allowed"}), 400
    
    try:
        # Secure filename and save
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract text from PDF
        text = ""
        try:
            with pdfplumber.open(filepath) as pdf:
                text = " ".join(page.extract_text() for page in pdf.pages if page.extract_text())
        except Exception as e:
            return jsonify({"error": f"PDF processing failed: {str(e)}"}), 400
        
        # Process extracted text
        result = extract_entities(text)
        
        # Generate a session ID for this extraction
        session_id = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        result['session_id'] = session_id
        
        # Save temporary results (without creating download file yet)
        temp_path = os.path.join(app.config['OUTPUT_FOLDER'], f"temp_{session_id}.json")
        with open(temp_path, 'w') as f:
            json.dump(result, f, indent=2)
        
        # Clean up
        os.remove(filepath)
        
        return jsonify({
            **result,
            "session_id": session_id  # Return session ID for future reference
        })
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/save_edited', methods=['POST'])
def save_edited_data():
    """Handle saving of edited resume data"""
    try:
        data = request.get_json()
        
        if not data or 'session_id' not in data:
            return jsonify({"error": "Invalid data or missing session ID"}), 400
        
        session_id = data['session_id']
        temp_path = os.path.join(app.config['OUTPUT_FOLDER'], f"temp_{session_id}.json")
        
        # Verify the temporary file exists
        if not os.path.exists(temp_path):
            return jsonify({"error": "Session expired or invalid session ID"}), 404
        
        # Generate final filename
        output_filename = f"resume_data_{session_id}.json"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        # Save the edited data
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Remove the temporary file
        os.remove(temp_path)
        
        return jsonify({
            "status": "success",
            "message": "Resume data saved successfully",
            "download_filename": output_filename
        })
        
    except Exception as e:
        return jsonify({"error": f"Error saving edited data: {str(e)}"}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download generated JSON file"""
    try:
        return send_from_directory(
            app.config['OUTPUT_FOLDER'],
            filename,
            as_attachment=True,
            mimetype='application/json'
        )
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)