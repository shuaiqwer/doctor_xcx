import os

BASE_DIR = os.getcwd()
IMAGE_DIR = os.path.join(BASE_DIR, "static", "product_images")
pid = 235443600
product_img_dir = os.path.join(IMAGE_DIR, str(pid))

print(f"Checking dir: {product_img_dir}")

if os.path.exists(product_img_dir):
    files = os.listdir(product_img_dir)
    images = [f for f in files if f.lower().endswith('.jpg')]
    print(f"Found {len(images)} jpg files.")
    
    # 寻找主图 (0.jpg 或 0_xxx.jpg)
    main_image = ""
    for img in images:
        if img.startswith('0.') or img.startswith('0_'):
            main_image = f"/static/product_images/{pid}/{img}"
            break
    print(f"Main image: {main_image}")
    
    # 寻找详情图 (1_xxx.jpg, 2_xxx.jpg ...)
    indexed_images = []
    for img in images:
        parts = img.split('_')
        try:
            index = int(parts[0])
            if index > 0: # 0是主图，详情图从1开始
                indexed_images.append((index, img))
        except ValueError:
            # 尝试直接解析文件名 1.jpg
            try:
                index = int(img.split('.')[0])
                if index > 0:
                    indexed_images.append((index, img))
            except:
                pass
    
    # 按索引排序
    indexed_images.sort(key=lambda x: x[0])
    detail_images = [f"/static/product_images/{pid}/{img[1]}" for img in indexed_images]
    print(f"Detail images count: {len(detail_images)}")
    print(detail_images)
else:
    print("Directory not found")
