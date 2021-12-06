from requests.structures import CaseInsensitiveDict
import requests
import json

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"

def get_cart_product_table(backend_url,timestamp):
    try:
        url = f'{backend_url}/cart-product-table/{timestamp}'
        res = requests.get(url)
        if res.status_code == 200:
            return json.loads(res.text), 200
        else:
            return None, res.status_code
    except:
        return None, 500

def get_cart_product(backend_url,idCart,idProduct):
    try:
        url = f'{backend_url}/cart/{idCart}/product/{idProduct}'
        res = requests.get(url)
        if res.status_code == 200:
            return json.loads(res.text), 200
        else:
            return None, res.status_code
    except:
        return None, 500

def insert_cart_product(backend_url,cartId,productId,body):
    try:
        url = f'{backend_url}/cart/{cartId}/product/{productId}'
        res = requests.post(url, headers=headers, data=json.dumps(body))
        if res.status_code == 201:
            return json.loads(res.text), 201
        else:
            return None, 400
    except:
        return None, 500