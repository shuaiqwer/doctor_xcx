import json
import os

product_id = '235443596'
json_path = f'd:\\doctor_xcx\\static\\data\\details\\{product_id}.json'
images_dir = f'd:\\doctor_xcx\\static\\product_images\\{product_id}'

def fix_xcx_field():
    if not os.path.exists(json_path): return
    
    # Get local files starting with 0_ 1_ etc.
    files = [f for f in os.listdir(images_dir) if f[0].isdigit() and f.endswith('.jpg') and not f.startswith('header')]
    # Sort them by number
    files.sort(key=lambda x: int(x.split('_')[0]))
    
    local_paths = [f'/static/product_images/{product_id}/{f}' for f in files]
    print(f"Assigning {len(local_paths)} images to xcx_detail_images")

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    product = data[0] if isinstance(data, list) else data
    product['xcx_detail_images'] = local_paths
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Fixed.")

if __name__ == '__main__':
    fix_xcx_field()
