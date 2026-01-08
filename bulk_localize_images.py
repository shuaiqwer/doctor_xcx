import os
import json
import requests
import re
import time
import random
from urllib.parse import urlparse
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# --- 配置 ---
BASE_DIR = r"d:\doctor_xcx"
DETAILS_DIR = os.path.join(BASE_DIR, "static", "data", "details")
PRODUCTS_LIST_PATH = os.path.join(BASE_DIR, "static", "data", "products.json")
IMAGE_SAVE_DIR = os.path.join(BASE_DIR, "static", "product_images")

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

def get_image_urls_from_html(html):
    if not html: return []
    html = str(html).replace("&#60;", "<").replace("&#62;", ">").replace("&#34;", '"').replace("&quot;", '"')
    urls = re.findall(r'src=["\'](https?://[^"\']+)["\']', html)
    return list(set(urls))

def download_image(url, save_path):
    try:
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Referer": "https://www.dinghuo123.com/",
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"
        }
        response = session.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            return True
        return False
    except:
        return False

def process_product(product_id):
    detail_path = os.path.join(DETAILS_DIR, f"{product_id}.json")
    if not os.path.exists(detail_path): return False
    with open(detail_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    product_data = data[0] if isinstance(data, list) else data
    
    all_urls = []
    desc_html = product_data.get("description", "") or product_data.get("introduction", "")
    all_urls.extend(get_image_urls_from_html(desc_html))
    
    album = product_data.get("album", [])
    if isinstance(album, list):
        for u in album:
            if not u: continue
            if u.startswith("http"): all_urls.append(u)
            elif "/" in str(u): all_urls.append("https://img.dinghuo123.com/" + str(u))
    
    main_img = product_data.get("imgUrl", "")
    if main_img:
        if not main_img.startswith("http") and "/" in str(main_img): 
            all_urls.append("https://img.dinghuo123.com/" + str(main_img))
        elif main_img.startswith("http"):
            all_urls.append(main_img)

    unique_urls = []
    seen = set()
    for u in all_urls:
        if u not in seen:
            unique_urls.append(u)
            seen.add(u)
    
    if not unique_urls: return False
    
    product_img_dir = os.path.join(IMAGE_SAVE_DIR, str(product_id))
    os.makedirs(product_img_dir, exist_ok=True)
    
    xcx_detail_images = []
    for i, url in enumerate(unique_urls):
        url_path = urlparse(url).path
        filename_only = os.path.basename(url_path).split("@")[0]
        ext = os.path.splitext(filename_only)[1] or ".jpg"
        filename = f"{i}{ext}"
        save_path = os.path.join(product_img_dir, filename)
        
        success = download_image(url, save_path)
        if not success and "oss.dinghuo123.com" not in url:
            # 常见 DBID 2548203
            alt_url = f"https://oss.dinghuo123.com/product/detail/images/2548203/{filename_only}"
            success = download_image(alt_url, save_path)
        
        if success:
            xcx_detail_images.append(f"/static/product_images/{product_id}/{filename}")

    product_data["xcx_detail_images"] = xcx_detail_images
    if xcx_detail_images:
        product_data["album"] = xcx_detail_images[:5]
        product_data["imgUrl"] = xcx_detail_images[0].replace("/static/", "")
    
    with open(detail_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return True

def main():
    max_count = 1700 # 几乎处理全部
    with open(PRODUCTS_LIST_PATH, "r", encoding="utf-8") as f:
        root_data = json.load(f)
    
    products = root_data["data"]["list"]
    count = 0
    for item in products:
        pid = str(item.get("id"))
        
        # 检查是否已本地化 (通过 previews 检查)
        if item.get("image", "").startswith("/static/"): continue
        
        print(f"[{count+1}] Processing Product {pid}...")
        if process_product(pid):
            detail_path = os.path.join(DETAILS_DIR, f"{pid}.json")
            with open(detail_path, "r", encoding="utf-8") as f:
                d = json.load(f)
                d_obj = d[0] if isinstance(d, list) else d
                if d_obj.get("xcx_detail_images"):
                    item["image"] = d_obj["xcx_detail_images"][0]
            count += 1
            print(f"   Success.")
            time.sleep(1)
        
        if count % 20 == 0 and count > 0:
            # 定期写回列表以保存进度
            with open(PRODUCTS_LIST_PATH, "w", encoding="utf-8") as f:
                json.dump(root_data, f, ensure_ascii=False, indent=2)

        if count >= max_count: break
        
    with open(PRODUCTS_LIST_PATH, "w", encoding="utf-8") as f:
        json.dump(root_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
