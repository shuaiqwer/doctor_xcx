import os
import requests
import time
import json
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crawler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class DingHuoCrawler:
    def __init__(self):
        self.base_url = "https://agent.dinghuo123.com"
        self.session = requests.Session()
        self.storage_path = "E:/doctor_data"
        self.local_data_path = "d:/doctor/static/data/products.json"
        
        # 请求头
        self.headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'client-source': 'pc',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': self.base_url,
            'referer': f"{self.base_url}/old/product/product?action=summaryList",
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
            'x-requested-with': 'XMLHttpRequest'
        }
        
        self.setup_cookies()

    def setup_cookies(self):
        """设置最新 Cookie"""
        cookies_str = 'ydh_instance=2548203; ydh_userId=24501718; jwt=eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJDMTAxMTUyODczNyIsInN1YiI6IntcImRiaWRcIjoyNTQ4MjAzLFwic1wiOlwiUENcIixcInVpZFwiOjI0NTAxNzE4LFwidXNlck5hbWVcIjpcIkMxMDExNTI4NzM3XCIsXCJ1c2VyVHlwZVwiOjJ9IiwiZXhwIjoxNzY4MjIyMzcyfQ.oAggncEFoFXTiBfHA6CUOZUzUQ8RUFg3c-VLrKDmP3Q; aliyungf_tc=29769bcc1644eaeef856f7503dfcd5f64c8f4234631049e8ddc9343e4a42ea11; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22C1011528737%22%2C%22first_id%22%3A%2219b8e3725791a-0dbc279c8cbf508-4c657b58-3686400-19b8e37257a1173%22%2C%22props%22%3A%7B%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTliOGUzNzI1NzkxYS0wZGJjMjc5YzhjYmY1MDgtNGM2NTdiNTgtMzY4NjQwMC01OWI4ZTM3MjU3YTExNzMiLCIkaWRlbnRpdHlfbG9naW5faWQiOiJDMTAxMTUyODczNyJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22C1011528737%22%7D%7D; loginTime=2; ydhSession=f802ece3ceb0469386e5b608a310dd561767631916917; com.jiaxincloud.mcs.cookie.username=web30241657538564306; acw_tc=1a0c398517676341774107052e0062b9e443e768af42998f300c14417fd016; JSESSIONID=4E8F098D761330D5FE8D4424D98FDCF9'
        for item in cookies_str.split('; '):
            if '=' in item:
                parts = item.split('=', 1)
                if len(parts) == 2:
                    name, value = parts
                    self.session.cookies.set(name, value, domain='agent.dinghuo123.com')

    def fetch_all_products(self, page_size=100):
        """从接口抓取所有商品并保存到 E 盘和本地"""
        all_raw_products = []
        current_page = 1
        total_pages = 1
        url = f"{self.base_url}/product/product?action=getProductGroupBySummary"
        
        while current_page <= total_pages:
            logging.info(f"正在抓取第 {current_page} 页...")
            data = {
                'orderby': '0',
                'currentPage': str(current_page),
                'pageSize': str(page_size)
            }
            try:
                response = self.session.post(url, data=data, headers=self.headers)
                res_json = response.json()
                if res_json.get("code") == 200:
                    page_data = res_json.get("data", {})
                    raw_items = page_data.get("items", [])
                    for sub_list in raw_items:
                        if isinstance(sub_list, list):
                            all_raw_products.extend(sub_list)
                    total_count = page_data.get("totalCount", 0)
                    total_pages = (total_count + page_size - 1) // page_size
                    logging.info(f"当前累计 {len(all_raw_products)}/{total_count}")
                    if not raw_items: break
                else:
                    logging.error(f"获取失败: {res_json.get('message')}")
                    break
            except Exception as e:
                logging.error(f"异常: {str(e)}")
                break
            current_page += 1
            time.sleep(0.3)
            
        # 保存原始数据到 E 盘
        e_raw_path = os.path.join(self.storage_path, "all_products_full.json")
        os.makedirs(os.path.dirname(e_raw_path), exist_ok=True)
        with open(e_raw_path, 'w', encoding='utf-8') as f:
            json.dump(all_raw_products, f, ensure_ascii=False, indent=2)
        
        return self.sync_from_e_drive()

    def sync_from_e_drive(self):
        """从 E 盘的原始数据同步到小程序的 products.json"""
        source_path = os.path.join(self.storage_path, "all_products_full.json")
        if not os.path.exists(source_path):
            logging.error(f"源文件不存在: {source_path}")
            return

        logging.info(f"正在从 {source_path} 同步数据...")
        with open(source_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        processed = self.process_products(raw_data)
        
        final_data = {
            "code": 200,
            "msg": "success",
            "data": {
                "list": processed,
                "total": len(processed),
                "updateTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }

        os.makedirs(os.path.dirname(self.local_data_path), exist_ok=True)
        with open(self.local_data_path, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=2)
        
        # 同时保存一份处理后的到 E 盘 (后端存储)
        e_processed_path = os.path.join(self.storage_path, "products.json")
        try:
            with open(e_processed_path, 'w', encoding='utf-8') as f:
                json.dump(final_data, f, ensure_ascii=False, indent=2)
            logging.info(f"处理后的数据已备份至: {e_processed_path}")
        except Exception as e:
            logging.warning(f"备份到 E 盘失败: {str(e)}")
        
        logging.info(f"同步完成，共 {len(processed)} 个商品已更新至小程序")
        return final_data

    def process_products(self, raw_items):
        processed = []
        for item in raw_items:
            try:
                # 1. 计算价格
                purchase_price = 0
                if item.get('priceList') and len(item['priceList']) > 0:
                    try:
                        # 尝试获取第一个规格的价格
                        purchase_price = float(item['priceList'][0]['unitPrices'][0]['orderPrice'])
                    except: pass

                display_price = 0
                # 优先使用 unitList 中的 orderPrice (通常是销售价)
                if item.get('unitList') and len(item['unitList']) > 0:
                    try:
                        display_price = float(item['unitList'][0]['orderPrice'])
                    except: pass
                
                # 如果销售价低于或等于进货价，或者销售价为0，则根据进货价加价
                if display_price <= purchase_price or display_price == 0:
                    if purchase_price > 0:
                        display_price = round(purchase_price * 1.3) # 默认加价 30%
                    else:
                        display_price = 99 # 兜底价格

                # 2. 构造对象
                p = {
                    "id": item.get('id'), # 使用 productId 确保与详情文件一致
                    "brand": item.get('brandName', '医美严选'),
                    "name": item.get('name'),
                    "price": str(display_price),
                    "purchasePrice": str(purchase_price),
                    "originalPrice": str(round(display_price * 1.5)),
                    "tags": ["热销", "正品保障"],
                    "image": "",
                    "sales": item.get('saleCount', 100)
                }

                # 图片处理 - 修复图片丢失问题
                if item.get('mainImg'):
                    # 优先使用原图，如果没有则使用 480 规格
                    img_url = item['mainImg'].get('imgUrl') or item['mainImg'].get('imgUrl_480')
                    if img_url:
                        # 确保 URL 完整
                        if not img_url.startswith('http'):
                            p["image"] = f"https://img.dinghuo123.com/{img_url}"
                        else:
                            p["image"] = img_url
                
                # 如果还是没图片，尝试从详情中提取（如果有的话）
                if not p["image"] and item.get('imgList') and len(item['imgList']) > 0:
                    img_url = item['imgList'][0].get('imgUrl')
                    if img_url:
                        p["image"] = f"https://img.dinghuo123.com/{img_url}" if not img_url.startswith('http') else img_url

                processed.append(p)
            except:
                continue
        return processed

    def fetch_product_detail(self, product_id):
        """获取单个商品的详情（包含描述）"""
        url = f"{self.base_url}/product/product?action=getProductWithDesc"
        data = {
            'submitType': 'ajax',
            'timeSort': 'asc',
            'id': str(product_id)
        }
        
        # 更新 Referer 为详情页
        headers = self.headers.copy()
        headers['referer'] = f"{self.base_url}/old/product/product?action=load&productId={product_id}"
        
        try:
            response = self.session.post(url, data=data, headers=headers)
            res_json = response.json()
            if res_json.get("code") == 200:
                return res_json.get("data")
            else:
                logging.error(f"获取详情失败 [{product_id}]: {res_json.get('message')}")
        except Exception as e:
            logging.error(f"请求详情异常 [{product_id}]: {str(e)}")
        return None

    def fetch_all_details(self, limit=None):
        """抓取所有商品的详情并保存"""
        source_path = os.path.join(self.storage_path, "all_products_full.json")
        if not os.path.exists(source_path):
            logging.error("请先运行 fetch_all_products 获取商品列表")
            return

        with open(source_path, 'r', encoding='utf-8') as f:
            products = json.load(f)

        if limit:
            products = products[:limit]

        logging.info(f"开始抓取 {len(products)} 个商品的详情...")
        
        e_detail_dir = os.path.join(self.storage_path, "details")
        local_detail_dir = "d:/doctor/static/data/details"
        os.makedirs(e_detail_dir, exist_ok=True)
        os.makedirs(local_detail_dir, exist_ok=True)

        count = 0
        for p in products:
            # 使用 top-level id (即 productId)，这是详情接口需要的
            pid = p.get('id')
            if not pid: continue
            
            # 检查是否已存在，避免重复抓取
            e_file = os.path.join(e_detail_dir, f"{pid}.json")
            if os.path.exists(e_file):
                continue

            detail = self.fetch_product_detail(pid)
            if detail:
                # 保存到 E 盘
                with open(e_file, 'w', encoding='utf-8') as f:
                    json.dump(detail, f, ensure_ascii=False, indent=2)
                
                # 保存到本地 static
                local_file = os.path.join(local_detail_dir, f"{pid}.json")
                with open(local_file, 'w', encoding='utf-8') as f:
                    json.dump(detail, f, ensure_ascii=False, indent=2)
                
                count += 1
                if count % 10 == 0:
                    logging.info(f"已抓取 {count} 个详情...")
                
                time.sleep(0.2) # 稍微延迟，避免被封
            
        logging.info(f"详情抓取完成，本次新增 {count} 个")

if __name__ == "__main__":
    crawler = DingHuoCrawler()
    # 1. 同步商品列表
    e_path = "E:/doctor_data/all_products_full.json"
    if os.path.exists(e_path):
        logging.info("检测到 E 盘已有数据，正在执行同步...")
        crawler.sync_from_e_drive()
    else:
        logging.info("E 盘无数据，开始从接口抓取...")
        crawler.fetch_all_products()
    
    # 2. 抓取商品详情 (全量抓取)
    # 已抓取的会自动跳过，支持断点续传
    crawler.fetch_all_details()

