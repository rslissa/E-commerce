from requests.structures import CaseInsensitiveDict
import requests
import json

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"


def get_product(backend_url, product_id):
    try:
        url = f'{backend_url}/product/{product_id}'
        res = requests.get(url)
        if res.status_code == 200:
            return json.loads(res.text), 200
        else:
            return None, res.status_code
    except:
        return None, 500


def list_products(backend_url):
    try:
        url = f'{backend_url}/list-products'
        res = requests.get(url)
        if res.status_code == 200:
            return json.loads(res.text), 200
        else:
            return None, res.status_code
    except:
        return None, 500


def list_products_by_cart(backend_url, cart_id):
    try:
        url = f'{backend_url}/list-products-by-cart/{cart_id}'
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


def delete_product(backend_url, product_id):
    try:
        url = f'{backend_url}/product/{product_id}'
        res = requests.delete(url)
        return None, res.status_code
    except:
        return None, 500
