
import requests

url = "https://oss.dinghuo123.com/product/detail/images/2548203/0782312b-edb3-4100-b8d9-ab38375c92db.png"

headers_empty = {
    "Referer": ""
}

headers_wx = {
    "Referer": "https://servicewechat.com/wx79afd16618dda3ac/devtools/page-frame.html"
}

def check(name, h):
    try:
        r = requests.head(url, headers=h, timeout=5)
        print(f"[{name}] Status: {r.status_code}")
    except Exception as e:
        print(f"[{name}] Error: {e}")

check("Empty Referer", headers_empty)
check("WeChat Referer", headers_wx)
