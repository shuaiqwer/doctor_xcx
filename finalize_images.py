import json
import os
import requests

product_id = '235443596'
json_path = f'd:\\doctor_xcx\\static\\data\\details\\{product_id}.json'
images_dir = f'd:\\doctor_xcx\\static\\product_images\\{product_id}'

def finalize_images():
    if not os.path.exists(json_path): return
    os.makedirs(images_dir, exist_ok=True)
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    product = data[0] if isinstance(data, list) else data

    headers = {'User-Agent': 'Mozilla/5.0'}
    base = "https://img.dinghuo123.com/"

    # 1. Main Image
    main_img_url_part = product.get('mainImg', {}).get('imgUrl', product.get('imgUrl', ''))
    if main_img_url_part and not main_img_url_part.startswith('/'):
        url = base + main_img_url_part
        filename = f"main_{os.path.basename(main_img_url_part.split('@')[0])}"
        dest = os.path.join(images_dir, filename)
        if not os.path.exists(dest):
            print(f"Downloading main image {url}...")
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                with open(dest, 'wb') as f: f.write(r.content)
        
        local_path = f"/static/product_images/{product_id}/{filename}"
        product['image'] = local_path # Top level
        if 'mainImg' in product: product['mainImg']['imgUrl'] = local_path
        product['imgUrl'] = local_path

    # 2. Album
    album = product.get('album', [])
    new_album = []
    for i, img_path in enumerate(album):
        if img_path.startswith('/'):
            new_album.append(img_path)
            continue
            
        url = img_path if img_path.startswith('http') else base + img_path
        filename = f"header_{i}_{os.path.basename(img_path.split('@')[0])}"
        dest = os.path.join(images_dir, filename)
        
        if not os.path.exists(dest):
             print(f"Downloading header {url}...")
             r = requests.get(url, headers=headers)
             if r.status_code == 200:
                 with open(dest, 'wb') as f: f.write(r.content)
        
        new_album.append(f"/static/product_images/{product_id}/{filename}")
    
    product['album'] = new_album

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Done")

if __name__ == '__main__':
    finalize_images()
