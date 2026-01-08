import json
import os

json_path = "static/data/details/235443600.json"

if os.path.exists(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                data = data[0]
            
            desc = data.get('description', '')
            img_count = desc.count('<img')
            print(f"Images in description HTML: {img_count}")
        except Exception as e:
            print(f"Error parsing JSON: {e}")
else:
    print("JSON file not found")
