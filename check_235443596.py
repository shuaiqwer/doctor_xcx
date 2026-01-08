import sqlite3
import json
import os

DB_PATH = "doctor_shop.db"
PID = 235443596
IMAGE_DIR = os.path.join(os.getcwd(), "static", "product_images", str(PID))

def check_all():
    results = {}
    
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        
        # Products table
        row = conn.execute("SELECT * FROM products WHERE id = ?", (PID,)).fetchone()
        if row: results['products_table'] = dict(row)
        
        # Details table
        d_row = conn.execute("SELECT * FROM product_details WHERE product_id = ?", (PID,)).fetchone()
        if d_row: results['details_table'] = {k: d_row[k] for k in d_row.keys() if k != 'raw_json'}
        
        conn.close()

    # Image directory
    if os.path.exists(IMAGE_DIR):
        files = os.listdir(IMAGE_DIR)
        results['local_images'] = [f for f in files if f.lower().endswith('.jpg')]
    else:
        results['local_images'] = "Directory not found"

    print(json.dumps(results, ensure_ascii=False, indent=2))

check_all()
