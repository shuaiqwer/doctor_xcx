import sqlite3
import json
import os

DB_PATH = "doctor_shop.db"
PID = 235443600

def check_product_details():
    if not os.path.exists(DB_PATH):
        print("Database not found")
        return
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM product_details WHERE product_id = ?", (PID,)).fetchone()
    conn.close()
    
    if row:
        detail = dict(row)
        print(f"ID: {detail['product_id']}")
        if detail['description']:
            print(f"Desc Img Count: {detail['description'].count('<img')}")
        else:
            print("Desc is empty")
        
        import json
        xcx_imgs = json.loads(detail['xcx_detail_images']) if detail['xcx_detail_images'] else []
        print(f"XCX Img Count: {len(xcx_imgs)}")
    else:
        print(f"No entry found in product_details for ID {PID}")

check_product_details()
