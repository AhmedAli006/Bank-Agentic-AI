import sqlite3

conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    cnic TEXT,
    email TEXT,
    phone TEXT,
    username TEXT,
    password TEXT
)
""")

conn.commit()

def save_user(data):
    try:
        cursor.execute("""
        INSERT INTO users (full_name, cnic, email, phone, username, password)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data["full_name"],
            data["cnic"],
            data["email"],
            data["phone"],
            data["username"],
            data["password"]
        ))
        conn.commit()
        print(f"✅ User {data['username']} saved to database successfully")
        return True
    except Exception as e:
        print(f"❌ Error saving user to database: {str(e)}")
        conn.rollback()
        return False