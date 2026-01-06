import requests
import json

def test_sso_and_products():
    sso_url = "https://sso.dinghuo123.com/jwtToken"
    product_url = "https://agent.dinghuo123.com/product/product?action=getProductGroupBySummary"
    
    sso_headers = {
        "Host": "sso.dinghuo123.com",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.7(0x13080712) UnifiedPCMacWechat(0xf264160c) XWEB/18056",
        "xweb_xhr": "1",
        "content-type": "application/json",
        "accept": "*/*",
        "referer": "https://servicewechat.com/wx79afd16618dda3ac/22/page-frame.html",
        "accept-language": "zh-CN,zh;q=0.9"
    }
    
    sso_data = {
        "dbid": "2548203",
        "limitClient": 1,
        "openId": "oNhz74qWS-UMvJulMhKGDSTMXaYg",
        "appId": "wx79afd16618dda3ac",
        "isWechat": False,
        "loginServerType": 1,
        "userName": "1K/9Mne22mOa2NVPlG0ekg==",
        "loginType": 3,
        "client": "miniApp",
        "source": 4
    }
    
    print("--- 尝试 SSO 登录 ---")
    session = requests.Session()
    response = session.post(sso_url, headers=sso_headers, json=sso_data)
    print(f"SSO 状态码: {response.status_code}")
    print(f"SSO 响应内容: {response.text}")
    print(f"SSO 响应 Cookies: {session.cookies.get_dict()}")
    
    res_json = response.json()
    if res_json.get("code") == 200 and res_json.get("data") and res_json["data"].get("jwtToken"):
        jwt = res_json["data"]["jwtToken"]
        print(f"\n成功获取 JWT: {jwt[:50]}...")
        
        # 关键步骤：先访问业务域的首页或特定接口，建立 Session
        print("\n--- 步骤 2: 访问业务域建立会话 ---")
        jump_url = f"https://agent.dinghuo123.com/login/login?jwt={jwt}"
        session.get(jump_url, headers={"User-Agent": sso_headers["user-agent"]})
        print(f"当前会话 Cookies: {session.cookies.get_dict()}")
        
        product_headers = {
            "Host": "agent.dinghuo123.com",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": "https://agent.dinghuo123.com/product/product",
            "X-Requested-With": "XMLHttpRequest"
        }
        
        # 尝试在 Cookie 中也带上 jwt
        session.cookies.set("jwt", jwt, domain="dinghuo123.com")
        session.cookies.set("ydh_instance", "2548203", domain="dinghuo123.com")
        
        product_data = {
            "action": "getProductGroupBySummary",
            "orderby": 0,
            "productTypeId": "",
            "productTypeIds": "[]",
            "keyword": "",
            "forward": "",
            "tagIds": "[]",
            "productBrandIds": "[]",
            "inventoyStatus": "",
            "currentPage": 1,
            "pageSize": 10
        }
        
        print("\n--- 尝试获取商品列表 ---")
        prod_res = session.post(product_url, headers=product_headers, data=product_data)
        print(f"商品接口状态码: {prod_res.status_code}")
        print(f"商品接口响应预览: {prod_res.text[:500]}")
    else:
        print("\nSSO 登录失败，无法继续测试商品接口。")

if __name__ == "__main__":
    test_sso_and_products()
