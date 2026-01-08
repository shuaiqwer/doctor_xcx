
import requests

# From JSON scan: https://oss.dinghuo123.com/product/detail/images/2548203/0782312b-edb3-4100-b8d9-ab38375c92db.png
oss_url = "https://oss.dinghuo123.com/product/detail/images/2548203/0782312b-edb3-4100-b8d9-ab38375c92db.png"
img_url = "https://img.dinghuo123.com/product/detail/images/2548203/0782312b-edb3-4100-b8d9-ab38375c92db.png"

def check(url):
    try:
        r = requests.head(url, timeout=5)
        print(f"URL: {url} -> Status: {r.status_code}")
    except Exception as e:
        print(f"URL: {url} -> Error: {e}")

print("Checking OSS URL...")
check(oss_url)
print("Checking IMG URL (substituted)...")
check(img_url)
