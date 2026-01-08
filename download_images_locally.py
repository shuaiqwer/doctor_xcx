
import json
import re
import os
import requests
import time

# Configuration
target_id = '235443596'
json_path = fr'd:\doctor_xcx\static\data\details\{target_id}.json'
save_dir_rel = f'static/product_images/{target_id}'
save_dir_abs = fr'd:\doctor_xcx\{save_dir_rel}'

# Ensure directory exists
os.makedirs(save_dir_abs, exist_ok=True)

# Headers to mimic a browser/allow access
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': '' # Empty referer often bypasses hotlink protection
}

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Locate the object
    target_obj = None
    if isinstance(data, list):
        target_obj = data[0]
    elif isinstance(data, dict):
        if 'data' in data:
             if isinstance(data['data'], list):
                 target_obj = data['data'][0]
             else:
                 target_obj = data['data']
        else:
             target_obj = data

    if target_obj and 'description' in target_obj:
        desc = target_obj['description']
        # Clean entities
        desc = desc.replace('&#60;', '<').replace('&#62;', '>').replace('&#34;', '"')
        
        # Extract URLs
        urls = re.findall(r'src=["\']([^"\']+)["\']', desc)
        
        local_urls = []
        
        print(f"Found {len(urls)} images. Downloading to {save_dir_rel}...")
        
        for i, url in enumerate(urls):
            if url.startswith('//'):
                url = 'https:' + url
                
            # Filename
            filename = f"{i}_{os.path.basename(url.split('?')[0])}"
            if not filename.lower().endswith(('.jpg', '.png', '.jpeg', '.gif')):
                filename += '.jpg'
                
            file_save_path = os.path.join(save_dir_abs, filename)
            
            # Download
            try:
                print(f"Downloading: {url}")
                r = requests.get(url, headers=headers, timeout=10)
                if r.status_code == 200:
                    with open(file_save_path, 'wb') as img_f:
                        img_f.write(r.content)
                    # Create the relative path for the uni-app project (absolute path starting with /)
                    # Note: In uni-app, /static references the static directory
                    local_url = f"/{save_dir_rel}/{filename}"
                    local_urls.append(local_url)
                else:
                    print(f"Failed to download {url}: Status {r.status_code}")
                    # Fallback to original if download fails
                    local_urls.append(url)
            except Exception as e:
                print(f"Error downloading {url}: {e}")
                local_urls.append(url)
                
            time.sleep(0.1) # Be nice

        # Update JSON
        target_obj['xcx_detail_images'] = local_urls
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print("Success! JSON updated with local paths.")

except Exception as e:
    print(f"Critical Error: {e}")
