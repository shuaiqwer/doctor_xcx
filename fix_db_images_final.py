import sqlite3
import os

# --- 配置 (请根据实际情况修改) ---
BASE_DIR = r"D:\doctor_xcx"
DB_PATH = os.path.join(BASE_DIR, "doctor_shop.db")
IMAGE_ROOT = os.path.join(BASE_DIR, "static", "product_images")

def fix_db_image_paths():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("开始扫描数据库商品路径...")
    cursor.execute("SELECT id, name, image FROM products")
    rows = cursor.fetchall()
    
    fixed_count = 0
    for pid, name, current_img in rows:
        product_dir = os.path.join(IMAGE_ROOT, str(pid))
        
        if os.path.exists(product_dir):
            # 寻找本地主图
            local_file = ""
            for f in os.listdir(product_dir):
                if f.startswith('0.') or f.startswith('0_'):
                    local_file = f
                    break
            
            if local_file:
                # 构造标准本地路径
                new_path = f"/static/product_images/{pid}/{local_file}"
                
                # 如果当前数据库路径不是这个，则更新
                if current_img != new_path:
                    cursor.execute("UPDATE products SET image = ? WHERE id = ?", (new_path, pid))
                    fixed_count += 1
                    if fixed_count % 50 == 0:
                        print(f"  已修正 {fixed_count} 个路径...")
        
    conn.commit()
    conn.close()
    print(f"完成！共修正 {fixed_count} 条商品路径，现在它们全部指向本地已存在的文件。")

if __name__ == "__main__":
    fix_db_image_paths()
