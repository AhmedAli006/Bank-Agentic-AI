import smtplib
from email.mime.text import MIMEText
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT

def send_email(to_email, username, password):
    """
    Send confirmation email with credentials to user.
    Returns True if successful, False otherwise.
    """
    try:
        msg = MIMEText(
            f"""
Your bank account has been created successfully!

Username: {username}
Password: {password}

Please change your password after first login.
"""
        )

        msg["Subject"] = "Your Bank Account Credentials"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email

        print(f"📧 Sending confirmation email to {to_email}...")
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Confirmation email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Error sending confirmation email to {to_email}: {str(e)}")
        return False