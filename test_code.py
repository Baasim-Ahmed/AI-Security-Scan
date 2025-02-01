# 🚨 Vulnerable Python Code - Hardcoded Password & SQL Injection
import sqlite3

# ⚠️ Hardcoded password (Bad practice)
PASSWORD = "supersecret123"

# ⚠️ SQL Injection vulnerability
user_input = input("Enter username: ")
query = "SELECT * FROM users WHERE username = '" + user_input + "';"
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute(query)
result = cursor.fetchall()

print(result)
