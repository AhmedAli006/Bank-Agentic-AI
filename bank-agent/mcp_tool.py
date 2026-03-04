import re

def extract_user_data(email_text: str) -> dict:
    """
    MCP TOOL:
    Extract structured data from unstructured email
    """
    def extract_field(text, field_name):
        for line in text.split('\n'):
            # Skip lines that look like email headers (From:, To:, Date:, Subject:, etc.)
            if line.startswith(('From:', 'To:', 'Date:', 'Subject:', 'Cc:', 'Bcc:', 'Return-Path:', 'Received:')):
                continue
            # Look for the field name in the line
            if field_name in line and ':' in line:
                # Extract value after the colon
                value = line.split(':', 1)[1].strip()
                if value:  # Only return if not empty
                    return value
        return None
    
    # Extract email directly from the Email line (avoiding headers)
    email = extract_field(email_text, "Email")
    if email:
        # Make sure it's a valid email format
        email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", email)
        email = email_match.group(0) if email_match else email
    
    full_name = extract_field(email_text, "Name")
    cnic = extract_field(email_text, "CNIC")
    phone = extract_field(email_text, "Phone")
    
    print(f"DEBUG - Extracted email: {email}")
    
    return {
        "full_name": full_name,
        "cnic": cnic,
        "email": email,
        "phone": phone
    }