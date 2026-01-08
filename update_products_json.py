
import json
import os

products_path = r'd:\doctor_xcx\static\data\products.json'
target_id = 235443596
local_images_base = '/static/product_images/235443596/'

# List of files we compressed/verified
files = [
    "0_af1fc607-7617-4746-b92b-100f6c4c595c.jpg",
    "1_7d31a724-eb4c-422d-87d5-0a20a070884b.jpg",
    "2_1af6be04-cd14-489b-91a1-a400811e2c1f.jpg",
    "3_ef846ee9-9655-4d71-b41c-971295396a1e.jpg",
    "4_434be94e-d23f-4d6a-953f-72623b396cc7.jpg",
    "5_598f7198-ca1d-4716-a8d4-65efd52bed1a.jpg",
    "6_33428ec6-2d00-41a9-b276-c1ce13184ccd.jpg",
    "7_e9e534c8-4602-4b1e-a91b-db7eee88a60d.jpg",
    "8_941197e2-1387-4a78-a549-7709f56d49e5.jpg",
    "9_c0d1bfb8-2314-4c77-8e52-128a099dc95e.jpg",
    "10_a6ed55db-38b4-4542-96ce-8319b58e5ea0.jpg",
    "11_92696d84-9766-4437-b6ba-1ce3003e1257.jpg",
    "12_e9149f39-4b64-47f4-a6a4-0f9e6abfbf9d.jpg"
]

images = [local_images_base + f for f in files]

try:
    with open(products_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Find product in list
    items = data.get('data', {}).get('list', [])
    found = False
    for item in items:
        if str(item.get('id')) == str(target_id):
            item['xcx_detail_images'] = images
            found = True
            print(f"Updated product {target_id} in products.json")
            break
            
    if found:
        with open(products_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    else:
        print(f"Product {target_id} not found in products.json")

except Exception as e:
    print(f"Error: {e}")
