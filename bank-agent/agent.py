from llm import call_llm
from mcp_tool import extract_user_data
from credentials import generate_credentials
from database import save_user
from email_service import send_email

class BankAccountAgent:

    def handle_email(self, email_text: str, sender_email: str = None):
        try:
            # Step 1: Decide action
            print("🔄 Processing email...")
            decision = call_llm(
                f"User sent the following email:\n{email_text}\n"
                "Extract account opening information and proceed."
            )

            # Step 2: MCP extraction
            print("📝 Extracting user data from email...")
            user_data = extract_user_data(email_text)
            print(f"✓ User data extracted: {user_data['full_name']} ({user_data.get('email', 'No email in body')})")

            # Step 3: Generate credentials
            print("🔐 Generating credentials...")
            username, password = generate_credentials(user_data["full_name"])
            user_data["username"] = username
            user_data["password"] = password
            print(f"✓ Credentials generated - Username: {username}")

            db_email = sender_email if sender_email else user_data.get("email")
            
            # If we have both and they're different, log this information
            if sender_email and user_data.get("email") and sender_email != user_data["email"]:
                print(f"📧 Note: Email in body ({user_data['email']}) differs from sender email ({sender_email})")
                print(f"📧 Using sender email for database and confirmation: {sender_email}")
            
            # Update the email in user_data to use the sender's email
            if sender_email:
                user_data["email"] = sender_email
            
            # Step 4: Save to DB with the correct email
            print("💾 Saving credentials to database...")
            save_success = save_user(user_data)
            
            if save_success:
                print(f"✓ User credentials saved to database with email: {user_data['email']}")
            else:
                print(f"⚠️ Warning: Failed to save to database, but continuing with email sending...")

            # Step 6: Send confirmation to the determined email
            email_sent = send_email(db_email, username, password)
            
            if email_sent:
                return f"✅ Account successfully created and confirmation email sent to {db_email}."
            else:
                return f"⚠️ Account created and saved to database, but confirmation email could not be sent to {db_email}."
        
        except Exception as e:
            print(f"❌ Error processing email: {str(e)}")
            return f"Error processing email: {str(e)}"