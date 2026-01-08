import json
import os
import re
import requests

product_id = '235443596'
json_path = f'd:\\doctor_xcx\\static\\data\\details\\{product_id}.json'
images_dir = f'd:\\doctor_xcx\\static\\product_images\\{product_id}'

def download_and_update():
    if not os.path.exists(json_path):
        print(f"JSON file not found: {json_path}")
        return

    if not os.path.exists(images_dir):
        os.makedirs(images_dir, exist_ok=True)

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    product = data[0] if isinstance(data, list) else data
    
    # 1. Collect all potential remote URLs (Header + Description)
    urls_to_download = []
    
    # Header images (album)
    album = product.get('album', [])
    for url in album:
        if isinstance(url, str) and url.startswith('http'):
            urls_to_download.append(('album', url))
            
    # Description images
    description = product.get('description', '')
    desc_urls = re.findall(r'src=["\'](https?://[^"\']+)["\']', description)
    # Also handle escaped quotes in the raw JSON string if needed, 
    # but since we already loaded it as JSON, the entities are just characters.
    for url in desc_urls:
        urls_to_download.append(('desc', url))

    # Download and Map
    # To keep names clean, we'll use a index-based prefix
    mapping = {}
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://servicewechat.com/' # Try to look like a mini program
    }

    print(f"Total URLs to process: {len(urls_to_download)}")
    
    for i, (tag, url) in enumerate(urls_to_download):
        try:
            filename = f"item_{i}_{os.path.basename(url.split('@')[0])}"
            if not filename.endswith(('.jpg', '.png', '.jpeg')):
                filename += ".jpg"
            
            filepath = os.path.join(images_dir, filename)
            local_path = f"/static/product_images/{product_id}/{filename}"
            
            if not os.path.exists(filepath):
                print(f"Downloading {url} ...")
                r = requests.get(url, headers=headers, timeout=10)
                if r.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(r.content)
                    print(f"Saved to {filepath}")
                else:
                    print(f"Failed to download {url}, status: {r.status_code}")
                    continue
            
            mapping[url] = local_path
        except Exception as e:
            print(f"Error processing {url}: {e}")

    # 2. Perform Replacements in JSON
    # Update album
    new_album = []
    for url in product.get('album', []):
        new_album.append(mapping.get(url, url))
    product['album'] = new_album
    
    # Update description
    new_description = description
    for remote_url, local_path in mapping.items():
        new_description = new_description.replace(remote_url, local_path)
    product['description'] = new_description

    # Update xcx_detail_images (for our specific logic)
    # Use only description images for the detail section
    xcx_images = []
    for tag, url in urls_to_download:
        if tag == 'desc' and url in mapping:
            xcx_images.append(mapping[url])
    product['xcx_detail_images'] = xcx_images

    # Update mainImg if needed
    if 'mainImg' in product and 'imgUrl' in product['mainImg']:
        # mainImg usually points to a partial path, not a full URL. 
        # But let's check if it's been updated to full URL by some process.
        pass

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("Update complete.")

if __name__ == '__main__':
    download_and_update()
