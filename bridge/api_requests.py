from requests.structures import CaseInsensitiveDict
import requests
import json

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"


def get_cart(backend_url, cartId):
    try:
        url = f'{backend_url}/cart/{cartId}'
        res = requests.get(url)
        if res.status_code == 200:
            return json.loads(res.text), 200
        else:
            return None, res.status_code
    except:
        return None, 500


def delete_cart_product(backend_url, cart_id):
    try:
        url = f'{backend_url}/cart/{cart_id}'
        res = requests.delete(url)
        return None, res.status_code
    except:
        return None, 500


def get_cart_product(backend_url, cart_id, product_id):
    try:
        url = f'{backend_url}/cart/{cart_id}/product/{product_id}'
        res = requests.get(url)
        if res.status_code == 200:
            return json.loads(res.text), 200
        else:
            return None, res.status_code
    except:
        return None, 500


def post_cart_product(backend_url, cart_id, product_id, body):
    try:
        url = f'{backend_url}/cart/{cart_id}/product/{product_id}'
        res = requests.post(url, headers=headers, data=json.dumps(body))
        if res.status_code == 201:
            return json.loads(res.text), 201
        else:
            return None, 400
    except:
        return None, 500


def delete_cart_product(backend_url, cart_id, product_id):
    try:
        url = f'{backend_url}/cart/{cart_id}/product/{product_id}'
        res = requests.delete(url)
        return None, res.status_code
    except:
        return None, 500


def get_cart_product_table(backend_url, timestamp):
    try:
        url = f'{backend_url}/cart-product-table/{timestamp}'
        res = requests.get(url)
        if res.status_code == 200:
            return json.loads(res.text), 200
        else:
            return None, res.status_code
    except:
        return None, 500


def insert_product(backend_url, body):
    try:
        url = f'{backend_url}/product'
        res = requests.post(url, headers=headers, data=json.dumps(body))
        if res.status_code == 201:
            return json.loads(res.text), 201
        else:
            return None, 400
    except:
        return None, 500
