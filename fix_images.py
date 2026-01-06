import json
import os
import subprocess
import logging
import time
import random

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_image_expert(url, product_id):
    local_dir = "d:/doctor/static/product_images"
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    
    filename = f"{product_id}.jpg"
    local_path = os.path.join(local_dir, filename)
    relative_path = f"/static/product_images/{filename}"
    
    # 专家级 curl 命令 (使用 curl.exe 避免 PowerShell 别名问题)
    curl_cmd = [
        'curl.exe', 
        '-s', '-L',
        '--connect-timeout', '15',
        '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        '-e', 'https://www.dinghuo123.com/',
        '--insecure',
        url,
        '-o', local_path
    ]
    
    try:
        # 如果文件已存在且大小正常，跳过
        if os.path.exists(local_path) and os.path.getsize(local_path) > 1000:
            return relative_path
            
        result = subprocess.run(curl_cmd, capture_output=True)
        if result.returncode == 0 and os.path.exists(local_path) and os.path.getsize(local_path) > 1000:
            logging.info(f"成功突破防盗链: {filename}")
            return relative_path
        else:
            logging.warning(f"下载失败: {url}")
            return url
    except Exception as e:
        logging.error(f"异常: {e}")
        return url

def fix_images():
    json_path = "d:/doctor/static/data/products.json"
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    count = 0
    total = len(data['products'])
    logging.info(f"开始修复 {total} 个商品的图片...")
    
    for product in data['products']:
        img_url = product.get('image', '')
        if img_url and img_url.startswith('http'):
            new_path = download_image_expert(img_url, product['id'])
            product['image'] = new_path
            count += 1
            if count % 5 == 0:
                logging.info(f"进度: {count}/{total}")
                # 随机延迟，防止被封IP
                time.sleep(random.uniform(0.5, 1.5))
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    logging.info("所有图片已成功本地化！")

if __name__ == "__main__":
    fix_images()
