import sqlite3
import json

conn = sqlite3.connect('doctor_shop.db')
conn.row_factory = sqlite3.Row
rows = conn.execute('SELECT id, name, image FROM products WHERE image IS NULL OR image = "" LIMIT 10').fetchall()
print(json.dumps([dict(r) for r in rows], ensure_ascii=False, indent=2))
conn.close()
