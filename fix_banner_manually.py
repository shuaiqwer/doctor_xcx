import json
import os

def fix_detail_json():
    detail_path = r'd:\doctor_xcx\static\data\details\235443596.json'
    
    with open(detail_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    product = data[0] if isinstance(data, list) else data
    
    # 既然描述图已经有了 13 张，我们拿前 3 张当作 Banner 图 (album)
    if 'xcx_detail_images' in product and len(product['xcx_detail_images']) >= 3:
        print("Setting album to first 3 detail images...")
        product['album'] = product['xcx_detail_images'][:3]
        product['imgUrl'] = product['xcx_detail_images'][0].replace('/static/', '') # 兼容 api.js 的 formatUrl
    
    with open(detail_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Fixed 235443596.json album fields.")

if __name__ == "__main__":
    fix_detail_json()
