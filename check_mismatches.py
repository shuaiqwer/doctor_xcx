import sqlite3
import os

DB_PATH = "doctor_shop.db"

def check_mismatches():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Find products where image is empty OR doesn't contain product_images
    rows = conn.execute("SELECT id, name, image FROM products").fetchall()
    conn.close()
    
    count = 0
    for row in rows:
        pid = row['id']
        image = row['image']
        folder_path = f"static/product_images/{pid}"
        has_folder = os.path.exists(folder_path)
        
        # If folder exists but image field is empty or points to remote
        if has_folder and (not image or 'product_images' not in image):
            print(f"Mismatch! ID: {pid} | Brand: {row['name'][:20]} | DB Image: {image} | Folder: EXISTS")
            count += 1
            if count > 20: break

check_mismatches()
