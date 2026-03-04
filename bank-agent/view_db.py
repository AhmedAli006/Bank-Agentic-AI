import sqlite3

conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

cursor.execute("SELECT id, full_name, cnic, email, phone, username FROM users")
rows = cursor.fetchall()

print("\nBank Account Records\n" + "-" * 40)

for row in rows:
    print(f"""
ID: {row[0]}
Name: {row[1]}
CNIC: {row[2]}
Email: {row[3]}
Phone: {row[4]}
Username: {row[5]}
""")

conn.close()
