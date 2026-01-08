import json
import os
import requests

product_id = '235443596'
json_path = f'd:\\doctor_xcx\\static\\data\\details\\{product_id}.json'
images_dir = f'd:\\doctor_xcx\\static\\product_images\\{product_id}'

def download_everything():
    if not os.path.exists(json_path): return
    os.makedirs(images_dir, exist_ok=True)
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    product = data[0] if isinstance(data, list) else data

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    base = "https://img.dinghuo123.com/"
    oss_base = "https://oss.dinghuo123.com/"

    # 1. Header/Banner Images (Album)
    # The JSON has albumList with partial paths
    album_list = product.get('albumList', [])
    new_album = []
    for i, item in enumerate(album_list):
        img_url_part = item.get('imgUrl', '')
        if not img_url_part: continue
        
        url = base + img_url_part
        filename = f"banner_{i}.jpg"
        dest = os.path.join(images_dir, filename)
        
        try:
            print(f"Downloading banner {url}...")
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                with open(dest, 'wb') as f: f.write(r.content)
            new_album.append(f"/static/product_images/{product_id}/{filename}")
        except Exception as e:
            print(f"Failed {url}: {e}")
            new_album.append(url)
    
    if new_album:
        product['album'] = new_album

    # 2. Main Image
    main_img_part = product.get('mainImg', {}).get('imgUrl', '')
    if main_img_part:
        url = base + main_img_part
        filename = "main_cover.jpg"
        dest = os.path.join(images_dir, filename)
        try:
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                with open(dest, 'wb') as f: f.write(r.content)
            product['image'] = f"/static/product_images/{product_id}/{filename}"
        except: pass

    # 3. Description Images (Migrate any remaining remote ones)
    description = product.get('description', '')
    # Remote images logic... we already localized them but let's make sure they are in xcx_detail_images
    
    # Get local files 0_ to 12_
    desc_files = [f for f in os.listdir(images_dir) if f[0].isdigit() and f.endswith('.jpg') and 'banner' not in f and 'main' not in f]
    desc_files.sort(key=lambda x: int(x.split('_')[0]))
    
    xcx_paths = [f'/static/product_images/{product_id}/{f}' for f in desc_files]
    product['xcx_detail_images'] = xcx_paths

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("All items processed.")

if __name__ == '__main__':
    download_everything()
