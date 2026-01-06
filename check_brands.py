import json
try:
    with open('d:/doctor/static/data/products.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    brands = {}
    for p in data['data']['list']:
        b = p.get('brand', '未知')
        brands[b] = brands.get(b, 0) + 1
    
    sorted_brands = sorted(brands.items(), key=lambda x: x[1], reverse=True)
    for b, count in sorted_brands[:30]:
        print(f"{b}: {count}")
except Exception as e:
    print(f"Error: {e}")
