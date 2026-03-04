import imaplib
import email
import time
import re
from agent import BankAccountAgent
from config import IMAP_SERVER, IMAP_EMAIL, IMAP_PASSWORD

TRIGGER_SUBJECT = "bank account opening request"
last_processed_email_id = None

def extract_email_from_header(from_header):
    """Extract clean email address from From header"""
    # Pattern to match email in angle brackets <email@example.com>
    match = re.search(r'<(.+?)>', from_header)
    if match:
        return match.group(1)
    # If no brackets, return the whole string (might already be just email)
    return from_header.strip()

def listen_for_emails():
    global last_processed_email_id
    agent = BankAccountAgent()
    
    print("🚀 Starting email listener... (Ctrl+C to stop)")
    
    while True:
        try:
            mail = imaplib.IMAP4_SSL(IMAP_SERVER)
            mail.login(IMAP_EMAIL, IMAP_PASSWORD)
            mail.select("inbox")

            # Get all emails and retrieve only the latest one
            status, messages = mail.search(None, "ALL")

            if status != "OK" or not messages[0]:
                print("⏳ No emails found in inbox. Checking again in 10 seconds...")
                mail.logout()
                time.sleep(10)
                continue

            # Get the latest email ID
            email_ids = messages[0].split()
            latest_email_id = email_ids[-1]

            # Skip if this is the email we already processed
            if latest_email_id == last_processed_email_id:
                print("⏳ No new emails. Checking again in 10 seconds...")
                mail.logout()
                time.sleep(10)
                continue

            print(f"📬 New email found! Checking latest email...")

            _, data = mail.fetch(latest_email_id, "(RFC822)")
            msg = email.message_from_bytes(data[0][1])

            subject = msg.get("Subject", "").lower()
            from_header = msg.get("From", "")
            
            # Extract clean sender email
            sender_email = extract_email_from_header(from_header)
            
            print(f"📧 Email from: {from_header}")
            print(f"📧 Clean sender email: {sender_email}")

            # ✅ SUBJECT-BASED TRIGGER - Check if latest email has trigger subject
            if TRIGGER_SUBJECT not in subject:
                print(f"⏭️  Email doesn't match trigger. Subject: {subject}")
                last_processed_email_id = latest_email_id
                mail.store(latest_email_id, "+FLAGS", "\\Seen")
                mail.logout()
                time.sleep(10)
                continue

            body = ""

            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        payload = part.get_payload(decode=True)
                        if payload:
                            body = payload.decode()
                        break
            else:
                payload = msg.get_payload(decode=True)
                if payload:
                    body = payload.decode()

            print(f"📧 Bank account opening email detected from: {sender_email}")
            
            # Pass both the email body and the sender's email to the agent
            result = agent.handle_email(body, sender_email)
            print(f"✨ Result: {result}")

            # Mark as read and save as processed
            mail.store(latest_email_id, "+FLAGS", "\\Seen")
            last_processed_email_id = latest_email_id

            mail.logout()
            print("✅ Email processing completed successfully")
            print("⏳ Listening for new emails... (Ctrl+C to stop)\n")
            time.sleep(10)
            
        except KeyboardInterrupt:
            print("\n🛑 Email listener stopped.")
            break
        except Exception as e:
            print(f"❌ Error in email listener: {str(e)}")
            try:
                mail.logout()
            except:
                pass
            print("⏳ Retrying in 10 seconds...\n")
            time.sleep(10)

if __name__ == "__main__":
    listen_for_emails()