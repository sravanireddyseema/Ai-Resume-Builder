def validate_resume_data(data):
    """Validate resume data before processing"""
    errors = []
    
    # Required fields - updated to match frontend form
    required_fields = ['name', 'email', 'phone', 'education', 'experience', 'skills', 'objective']
    for field in required_fields:
        if not data.get(field, '').strip():
            errors.append(f"{field.replace('_', ' ').title()} is required")
    
    # Field length validations
    if data.get('name') and len(data['name'].strip()) > 100:
        errors.append("Name must be less than 100 characters")
    
    if data.get('email') and len(data['email'].strip()) > 100:
        errors.append("Email must be less than 100 characters")
    
    if data.get('phone') and len(data['phone'].strip()) > 20:
        errors.append("Phone must be less than 20 characters")
    
    if data.get('education') and len(data['education'].strip()) > 1000:
        errors.append("Education must be less than 1000 characters")
    
    if data.get('experience') and len(data['experience'].strip()) > 2000:
        errors.append("Experience must be less than 2000 characters")
    
    if data.get('skills') and len(data['skills'].strip()) > 1000:
        errors.append("Skills must be less than 1000 characters")
    
    if data.get('objective') and len(data['objective'].strip()) > 500:
        errors.append("Objective must be less than 500 characters")
    
    return errors

def sanitize_input(text):
    """Basic input sanitization"""
    if not text:
        return ""
    
    # Remove potentially harmful characters but keep basic formatting
    dangerous_chars = ['<', '>', '"', "'", '`', '=', '$', '{', '}']
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    return text.strip()
