from datetime import datetime

import api_requests
from requests.structures import CaseInsensitiveDict

import requests
import json

first_backend = 'http://localhost:5001/bea/v1'
second_backend = 'http://localhost:5002/beb/v1'

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"


def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    shared_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    print(f"Presenti nel primo ma non nel secondo {added}")
    removed = d2_keys - d1_keys
    print(f"presenti nel secondo ma non nel primo {removed}")
    modified = {o: (d1[o], d2[o]) for o in shared_keys if d1[o] != d2[o]}
    print(f"modified {modified}")
    same = set(o for o in shared_keys if d1[o] == d2[o])
    print(f"same {same}")
    return added, removed, modified, same


def cart_product_synchronization(timestamp):
    rows_a = None
    try:
        # take the new rows of the cart_product table in the first Back-end
        rows_a = json.loads(requests.get(f'{first_backend}/cart-product-table/{timestamp}').text)
    except:
        print("first back-end unreachable")

    if rows_a is not None:
        for row_a in rows_a:
            # look if the new rows of the first back-end are present in the second back-end
            row_b = json.loads(
                requests.get(f'{second_backend}/cart/{row_a["id_cart"]}/product/{row_a["id_product"]}').text)
            if row_b is None:
                # if not present, insert it
                row_a['operation'] = 'add'
                res = requests.post(f'{second_backend}/cart/{row_a["id_cart"]}/product/{row_a["id_product"]}',
                                    headers=headers, data=json.dumps(row_a))
            if row_b is not None:
                # if present, it overwrites the one with the oldest timestamp
                last_update_a = datetime.strptime(row_a['last_update'], '%Y-%m-%dT%H:%M:%S.%f').timestamp()
                last_update_b = datetime.strptime(row_b['last_update'], '%Y-%m-%dT%H:%M:%S.%f').timestamp()
                if last_update_a != last_update_b or row_a != row_b:
                    if last_update_a >= last_update_b:
                        res = requests.put(f'{second_backend}/cart/{row_a["id_cart"]}/product/{row_a["id_product"]}',
                                           headers=headers, data=json.dumps(row_a))
                    elif last_update_a < last_update_b:
                        res = requests.put(f'{first_backend}/cart/{row_b["id_cart"]}/product/{row_b["id_product"]}',
                                           headers=headers, data=json.dumps(row_b))

    rows_b = None
    try:
        # take the new rows of the cart_product table in the second back-end
        rows_b = json.loads(requests.get(f'{second_backend}/cart-product-table/{timestamp}').text)
    except:
        print("second back-end unreachable")

    if rows_b is not None:
        for row_b in rows_b:
            # look if the new rows of the second back-end are present in the first back-end
            row_a = json.loads(
                requests.get(f'{first_backend}/cart/{row_b["id_cart"]}/product/{row_b["id_product"]}').text)
            if row_a is None:
                # if not present, insert it
                row_b['operation'] = 'add'
                res = requests.post(f'{first_backend}/cart/{row_b["id_cart"]}/product/{row_b["id_product"]}',
                                    headers=headers, data=json.dumps(row_b))
            if row_a is not None:
                # if present, it overwrites the one with the oldest timestamp
                last_update_a = datetime.strptime(row_a['last_update'], '%Y-%m-%dT%H:%M:%S.%f').timestamp()
                last_update_b = datetime.strptime(row_b['last_update'], '%Y-%m-%dT%H:%M:%S.%f').timestamp()
                if last_update_a != last_update_b or row_a != row_b:
                    if last_update_a > last_update_b:
                        res = requests.put(f'{second_backend}/cart/{row_a["id_cart"]}/product/{row_a["id_product"]}',
                                           headers=headers, data=json.dumps(row_a))
                    elif last_update_a < last_update_b:
                        res = requests.put(f'{first_backend}/cart/{row_b["id_cart"]}/product/{row_b["id_product"]}',
                                           headers=headers, data=json.dumps(row_b))







if __name__ == '__main__':
    while 1:
        timestamp = datetime.now()
        cart_product_synchronization(timestamp)


