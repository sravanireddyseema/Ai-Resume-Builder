from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import uuid
from validation import validate_resume_data, sanitize_input
from firebase_config import get_database
import os

app = Flask(__name__)
CORS(app)  # allow frontend to talk to backend

# Get Firebase Realtime Database
database = get_database()

@app.route("/")
def home():
    return "AI Resume Backend with Firebase Realtime Database is running"

@app.route("/generate_resume", methods=["POST"])
def generate_resume():
    if not database:
        return jsonify({"error": "Database not available"}), 500
    
    data = request.json
    
    # Validate input
    errors = validate_resume_data(data)
    if errors:
        return jsonify({"error": "Validation failed", "details": errors}), 400
    
    # Sanitize input
    name = sanitize_input(data.get("name", ""))
    email = sanitize_input(data.get("email", ""))
    phone = sanitize_input(data.get("phone", ""))
    education = sanitize_input(data.get("education", ""))
    experience = sanitize_input(data.get("experience", ""))
    skills = sanitize_input(data.get("skills", ""))
    objective = sanitize_input(data.get("objective", ""))
    template = data.get("template", "professional")
    
    # Generate resume text based on template
    resume_text = generate_resume_text(data, template)
    
    # Create resume data
    resume_id = str(uuid.uuid4())
    resume_data = {
        "id": resume_id,
        "name": name,
        "email": email,
        "phone": phone,
        "education": education,
        "experience": experience,
        "skills": skills,
        "objective": objective,
        "template": template,
        "resume_text": resume_text,
        "created_at": datetime.utcnow().isoformat()
    }
    
    # Save to Firebase Realtime Database
    try:
        database.child("resumes").child(resume_id).set(resume_data)
        return jsonify({
            "success": True,
            "resume_id": resume_id,
            "resume_text": resume_text
        })
    except Exception as e:
        return jsonify({"error": f"Failed to save resume: {str(e)}"}), 500

# Get all resumes
@app.route("/resumes", methods=["GET"])
def get_all_resumes():
    if not database:
        return jsonify({"error": "Database not available"}), 500
    
    try:
        resumes_ref = database.child("resumes").get()
        resumes = []
        
        if resumes_ref:
            for resume_id, resume_data in resumes_ref.items():
                if isinstance(resume_data, dict):
                    resume_data['id'] = resume_id
                    resumes.append(resume_data)
        
        # Sort by created_at (newest first)
        resumes.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return jsonify({"resumes": resumes})
    except Exception as e:
        print(f"Error fetching resumes: {e}")
        return jsonify({"error": "Failed to fetch resumes"}), 500

# Get a specific resume by ID
@app.route("/resumes/<resume_id>", methods=["GET"])
def get_resume(resume_id):
    if not database:
        return jsonify({"error": "Database not available"}), 500
    
    try:
        resume_ref = database.child("resumes").child(resume_id).get()
        
        if resume_ref:
            resume_data = resume_ref
            if isinstance(resume_data, dict):
                resume_data['id'] = resume_id
                return jsonify({"resume": resume_data})
            else:
                return jsonify({"error": "Invalid resume data"}), 500
        else:
            return jsonify({"error": "Resume not found"}), 404
    except Exception as e:
        print(f"Error fetching resume: {e}")
        return jsonify({"error": "Failed to fetch resume"}), 500

# Update a resume
@app.route("/resumes/<resume_id>", methods=["PUT"])
def update_resume(resume_id):
    if not database:
        return jsonify({"error": "Database not available"}), 500
    
    try:
        data = request.json
        
        # Validate input
        errors = validate_resume_data(data)
        if errors:
            return jsonify({"error": "Validation failed", "details": errors}), 400
        
        # Check if resume exists
        existing_resume = database.child("resumes").child(resume_id).get()
        if not existing_resume:
            return jsonify({"error": "Resume not found"}), 404
        
        # Sanitize input and update resume data
        name = sanitize_input(data.get("name", ""))
        email = sanitize_input(data.get("email", ""))
        phone = sanitize_input(data.get("phone", ""))
        education = sanitize_input(data.get("education", ""))
        experience = sanitize_input(data.get("experience", ""))
        skills = sanitize_input(data.get("skills", ""))
        objective = sanitize_input(data.get("objective", ""))
        template = data.get("template", "professional")
        
        # Regenerate resume text
        resume_text = generate_resume_text(data, template)
        
        update_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "education": education,
            "experience": experience,
            "skills": skills,
            "objective": objective,
            "template": template,
            "resume_text": resume_text,
            "updated_at": datetime.utcnow().isoformat()
        }
        
        database.child("resumes").child(resume_id).update(update_data)
        
        return jsonify({
            "success": True,
            "message": "Resume updated successfully!",
            "resume_text": resume_text
        })
    except Exception as e:
        print(f"Error updating resume: {e}")
        return jsonify({"error": "Failed to update resume"}), 500

# Delete a resume
@app.route("/resumes/<resume_id>", methods=["DELETE"])
def delete_resume(resume_id):
    if not database:
        return jsonify({"error": "Database not available"}), 500
    
    try:
        # Check if resume exists
        existing_resume = database.child("resumes").child(resume_id).get()
        if not existing_resume:
            return jsonify({"error": "Resume not found"}), 404
        
        database.child("resumes").child(resume_id).delete()
        
        return jsonify({"success": True, "message": "Resume deleted successfully!"})
    except Exception as e:
        print(f"Error deleting resume: {e}")
        return jsonify({"error": "Failed to delete resume"}), 500

# Chatbot endpoint
@app.route("/chatbot", methods=["POST"])
def chatbot():
    try:
        data = request.json
        user_message = sanitize_input(data.get("message", ""))
        
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        
        # Generate response based on keywords (simple implementation)
        response = generate_chatbot_response(user_message)
        
        return jsonify({
            "response": response,
            "status": "success"
        })
        
    except Exception as e:
        print(f"Error in chatbot: {e}")
        fallback_responses = [
            "I'm here to help with your resume building! Feel free to ask me about career advice, skill recommendations, or resume tips.",
            "As your AI resume assistant, I can help you create better resumes and provide career guidance. What would you like to know?",
            "I'm designed to help you build professional resumes and provide career insights. How can I assist you today?"
        ]
        
        import random
        return jsonify({
            "response": random.choice(fallback_responses),
            "status": "fallback"
        })

def generate_chatbot_response(message):
    """Generate chatbot response based on keywords"""
    lower_message = message.lower()
    
    if 'resume' in lower_message or 'cv' in lower_message:
        return "I can help you create a professional resume! Fill out the form with your details and click 'Generate Resume'. You can choose from Professional, Modern, or Executive templates."
    elif 'template' in lower_message:
        return "We offer three professional templates:\n\n**Professional**: Classic design for corporate positions\n**Modern**: Contemporary style for creative roles\n**Executive**: Sophisticated layout for leadership positions\n\nClick on any template to select it!"
    elif 'download' in lower_message or 'pdf' in lower_message:
        return "Once you generate your resume, a download button will appear below the preview. Click 'Download Resume as PDF' to get a professional PDF file!"
    elif 'help' in lower_message or 'how' in lower_message:
        return "I'm here to help with resume building! Here's what I can assist with:\n\n**Resume writing tips**\n**Template selection**\n**Content suggestions**\n**Download guidance**\n**Formatting advice**\n\nWhat would you like help with?"
    else:
        return "I'm here to help with resume building! Ask me about:\n• Resume templates\n• Writing tips for each section\n• Downloading your PDF\n• Best practices\n\nWhat would you like to know?"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)