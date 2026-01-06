import requests
import json

url = "https://agent.dinghuo123.com/product/product?action=getProductGroupBySummary"

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'client-source': 'pc',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://agent.dinghuo123.com',
    'referer': 'https://agent.dinghuo123.com/old/product/product?action=summaryList&keyword=%E8%83%B6%E5%8E%9F%E8%9B%8B%E7%99%BD',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
    'x-requested-with': 'XMLHttpRequest'
}

cookies = {
    'ydh_instance': '2548203',
    'ydh_userId': '24501718',
    'jwt': 'eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJDMTAxMTUyODczNyIsInN1YiI6IntcImRiaWRcIjoyNTQ4MjAzLFwic1wiOlwiUENcIixcInVpZFwiOjI0NTAxNzE4LFwidXNlck5hbWVcIjpcIkMxMDExNTI4NzM3XCIsXCJ1c2VyVHlwZVwiOjJ9IiwiZXhwIjoxNzY4MjIyMzcyfQ.oAggncEFoFXTiBfHA6CUOZUzUQ8RUFg3c-VLrKDmP3Q',
    'ydhSession': '2d56de48846442f68945e7818b5f96891767618040446',
    'JSESSIONID': 'A6B747D90B43567DCB72C5550DF2D88D',
    'acw_tc': 'ac11000117676304916912578e004e6a65332ad77c199e8f79d30c83854858'
}

data = {
    'orderby': '0',
    'productTypeId': '',
    'productTypeIds': '[]',
    'keyword': '胶原蛋白',
    'forward': '',
    'tagIds': '[]',
    'productBrandIds': '[]',
    'inventoyStatus': '',
    'currentPage': '1',
    'pageSize': '12'
}

url_cat = "https://agent.dinghuo123.com/product/product?action=getProductType"
response_cat = requests.get(url_cat, headers=headers, cookies=cookies)
print("Categories Response:")
print(json.dumps(response_cat.json(), ensure_ascii=False, indent=2)[:1000])
