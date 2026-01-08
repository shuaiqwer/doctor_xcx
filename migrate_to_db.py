import sqlite3
import json
import os
import glob

# --- 配置 ---
BASE_DIR = r"d:\doctor_xcx"
PRODUCTS_JSON = os.path.join(BASE_DIR, "static", "data", "products.json")
DETAILS_DIR = os.path.join(BASE_DIR, "static", "data", "details")
DB_PATH = os.path.join(BASE_DIR, "doctor_shop.db")

def init_db():
    """初始化数据库表结构"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建商品简表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        brand TEXT,
        name TEXT,
        price REAL,
        purchase_price REAL,
        original_price REAL,
        image TEXT,
        sales INTEGER,
        tags TEXT
    )
    ''')
    
    # 创建商品详情表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS product_details (
        product_id INTEGER PRIMARY KEY,
        description TEXT,
        album TEXT,
        xcx_detail_images TEXT,
        raw_json TEXT,
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
    ''')
    
    conn.commit()
    return conn

def migrate_data():
    conn = init_db()
    cursor = conn.cursor()
    
    # 1. 迁移产品列表
    print("Migrating products list...")
    if os.path.exists(PRODUCTS_JSON):
        with open(PRODUCTS_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
            products_list = data.get('data', {}).get('list', [])
            
            for p in products_list:
                tags_str = ",".join(p.get('tags', [])) if isinstance(p.get('tags'), list) else ""
                cursor.execute('''
                INSERT OR REPLACE INTO products (id, brand, name, price, purchase_price, original_price, image, sales, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    p.get('id'),
                    p.get('brand'),
                    p.get('name'),
                    p.get('price'),
                    p.get('purchasePrice'),
                    p.get('originalPrice'),
                    p.get('image'),
                    p.get('sales'),
                    tags_str
                ))
    
    # 2. 迁移产品详情
    print("Migrating product details (this may take a while)...")
    detail_files = glob.glob(os.path.join(DETAILS_DIR, "*.json"))
    
    count = 0
    for file_path in detail_files:
        try:
            pid = int(os.path.basename(file_path).replace('.json', ''))
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 详情 JSON 通常是一个包含单个字典的列表
                raw = data[0] if isinstance(data, list) and len(data) > 0 else data
                
                description = raw.get('description', '') or raw.get('introduction', '')
                album = json.dumps(raw.get('album', []), ensure_ascii=False)
                xcx_detail_images = json.dumps(raw.get('xcx_detail_images', []), ensure_ascii=False)
                raw_json = json.dumps(data, ensure_ascii=False)
                
                cursor.execute('''
                INSERT OR REPLACE INTO product_details (product_id, description, album, xcx_detail_images, raw_json)
                VALUES (?, ?, ?, ?, ?)
                ''', (pid, description, album, xcx_detail_images, raw_json))
                
                count += 1
                if count % 100 == 0:
                    print(f"  Processed {count} details...")
        except Exception as e:
            print(f"  Error processing {file_path}: {e}")
            
    conn.commit()
    conn.close()
    print(f"\nMigration complete! Total products/details migrated: {count}")
    print(f"Database saved to: {DB_PATH}")

if __name__ == "__main__":
    migrate_data()
