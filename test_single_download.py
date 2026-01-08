import requests

url = "https://img.dinghuo123.com/2548203/745fed4a-9d92-4ece-a31b-705acfd4ddb6.jpg"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "https://www.dinghuo123.com/"
}

try:
    print(f"Testing URL: {url}")
    r = requests.get(url, headers=headers, timeout=15)
    print(f"Status Code: {r.status_code}")
    print(f"Content Length: {len(r.content)}")
except Exception as e:
    print(f"Error: {e}")
