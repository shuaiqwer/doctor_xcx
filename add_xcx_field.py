
import json
import re
import os

file_path = r'd:\doctor_xcx\static\data\details\235443596.json'

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Handle array root or object root
    target_obj = None
    if isinstance(data, list):
        target_obj = data[0]
    elif isinstance(data, dict):
        if 'data' in data:
             # structure might be {code, data: {...}} or {code, data: [...]}
             if isinstance(data['data'], list):
                 target_obj = data['data'][0]
             else:
                 target_obj = data['data']
        else:
             target_obj = data

    if target_obj and 'description' in target_obj:
        desc = target_obj['description']
        # Decode HTML entities if present
        desc = desc.replace('&#60;', '<').replace('&#62;', '>').replace('&#34;', '"')
        
        # Regex to find img src
        # Matches <img src="URL">
        urls = re.findall(r'src=["\']([^"\']+)["\']', desc)
        
        # Clean URLs (remove domain if relative? No, they seem absolute)
        # Ensure they are accessible. 
        # The user said "make globally accessible". 
        # The current URLs are oss.dinghuo123.com.
        # If the user implies I should change them, I don't have a new domain.
        # I will populate the field with the extracted URLs.
        
        clean_urls = []
        for url in urls:
            if url.startswith('//'):
                url = 'https:' + url
            clean_urls.append(url)

        target_obj['xcx_detail_images'] = clean_urls
        print(f"Extracted {len(clean_urls)} images.")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print("Updated JSON with xcx_detail_images field.")

except Exception as e:
    print(f"Error: {e}")
