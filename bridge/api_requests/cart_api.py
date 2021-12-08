from requests.structures import CaseInsensitiveDict
import requests
import json

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"


def insert_cart(backend_url):
    try:
        url = f'{backend_url}/cart'
        res = requests.post(url, headers=headers)
        if res.status_code == 200:
            return json.loads(res.text), 201
        else:
            return None, 400
    except:
        return None, 500


def get_cart(backend_url, cart_id):
    try:
        url = f'{backend_url}/cart/{cart_id}'
        res = requests.get(url)
        if res.status_code == 200:
            return json.loads(res.text), 200
        else:
            return None, res.status_code
    except:
        return None, 500


def delete_cart(backend_url, cart_id):
    try:
        url = f'{backend_url}/cart/{cart_id}'
        res = requests.delete(url)
        return None, res.status_code
    except:
        return None, 500
