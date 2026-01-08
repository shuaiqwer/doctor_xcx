import sqlite3
import json
import os

DB_PATH = "doctor_shop.db"
JSON_PATH = "static/data/details/235443600.json"
PID = 235443600

def check_db():
    if not os.path.exists(DB_PATH):
        print("Database not found")
        return None
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM products WHERE id = ?", (PID,)).fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return None

def check_json():
    if not os.path.exists(JSON_PATH):
        print("JSON not found")
        return None
    
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        if isinstance(data, list):
            return data[0]
        return data

db_data = check_db()
json_data = check_json()

print("--- Database Data ---")
if db_data:
    print(json.dumps(db_data, ensure_ascii=False, indent=2))
else:
    print("Not found in DB")

print("\n--- JSON Source Data (Key Fields) ---")
if json_data:
    keys = ['id', 'name', 'productBrand', 'purchasePrice', 'marketPrice', 'tags']
    source_summary = {k: json_data.get(k) for k in keys if k in json_data}
    # purchasePrice might be missing in original JSON or named differently
    source_summary['costPrice'] = json_data.get('costPrice')
    source_summary['marketPrice'] = json_data.get('marketPrice')
    print(json.dumps(source_summary, ensure_ascii=False, indent=2))
else:
    print("Not found in JSON")
