from agent import BankAccountAgent

email_content = """
Name: Ahmed Ali
CNIC: 42101-1234567-1
Email: ahmed@gmail.com
Phone: 0301-1234567
"""

agent = BankAccountAgent()
result = agent.handle_email(email_content)

print(result)