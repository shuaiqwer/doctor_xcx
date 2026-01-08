import sqlite3
import os

DB_PATH = "doctor_shop.db"

if os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM products WHERE id = 235443600")
    row = cursor.fetchone()
    if row:
        print(f"Product found in DB: {row}")
    else:
        print("Product NOT found in DB")
    conn.close()
else:
    print("Database file not found")
