import json
import os
import requests

product_id = '235443596'
json_path = f'd:\\doctor_xcx\\static\\data\\details\\{product_id}.json'
images_dir = f'd:\\doctor_xcx\\static\\product_images\\{product_id}'

def download_headers():
    if not os.path.exists(json_path): return
    os.makedirs(images_dir, exist_ok=True)

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    product = data[0] if isinstance(data, list) else data

    # 1. Image URLs
    # Base URL for header images
    base = "https://img.dinghuo123.com/"
    album = product.get('album', [])
    
    new_album = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    for i, img_path in enumerate(album):
        if img_path.startswith('http'):
            url = img_path
        else:
            url = base + img_path
            
        filename = f"header_{i}_{os.path.basename(img_path.split('@')[0])}"
        local_path = f"/static/product_images/{product_id}/{filename}"
        dest = os.path.join(images_dir, filename)
        
        try:
            if not os.path.exists(dest):
                print(f"Downloading header {url}...")
                r = requests.get(url, headers=headers, timeout=10)
                if r.status_code == 200:
                    with open(dest, 'wb') as f:
                        f.write(r.content)
            new_album.append(local_path)
            print(f"Mapped {url} -> {local_path}")
        except:
            new_album.append(url)

    product['album'] = new_album

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Done")

if __name__ == '__main__':
    download_headers()
