import requests
import json

url = "https://agent.dinghuo123.com/product/product?action=getProductGroupBySummary"
headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
}
cookies = {
    'ydh_instance': '2548203',
    'ydh_userId': '24501718',
    'jwt': 'eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJDMTAxMTUyODczNyIsInN1YiI6IntcImRiaWRcIjoyNTQ4MjAzLFwic1wiOlwiUENcIixcInVpZFwiOjI0NTAxNzE4LFwidXNlck5hbWVcIjpcIkMxMDExNTI4NzM3XCIsXCJ1c2VyVHlwZVwiOjJ9IiwiZXhwIjoxNzY4MjIyMzcyfQ.oAggncEFoFXTiBfHA6CUOZUzUQ8RUFg3c-VLrKDmP3Q',
    'ydhSession': 'f802ece3ceb0469386e5b608a310dd561767631916917',
    'JSESSIONID': '8A6119F6742B2A8C8935144B4C325926'
}

url = "https://agent.dinghuo123.com/product/product?action=getProductType"
res = requests.get(url, headers=headers, cookies=cookies)
if res.status_code == 200:
    print("Categories:", json.dumps(res.json(), ensure_ascii=False, indent=2))
else:
    print("Error:", res.status_code)
