import sqlite3
import os

DB_PATH = "doctor_shop.db"
BASE_DIR = os.getcwd()

def check():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT id, name, image FROM products LIMIT 12").fetchall()
    conn.close()
    
    for row in rows:
        img_path = row['image']
        # Convert /static/product_images/... to local path
        if img_path and img_path.startswith('/static/'):
            local_path = os.path.join(BASE_DIR, img_path.lstrip('/').replace('/', os.sep))
            exists = os.path.exists(local_path)
            print(f"ID: {row['id']} | Image: {img_path} | Exists: {exists}")
        else:
            print(f"ID: {row['id']} | Image: {img_path} | INVALID PATH FORMAT")

check()
