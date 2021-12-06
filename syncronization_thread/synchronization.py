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


if __name__ == '__main__':
    # x = dict(a=1, b=2, c=4)
    # y = dict(a=2, b=2, d=4)
    # dict_compare(x,y)
    timestamp = datetime.now()

    # print(type(timestamp.strftime("%Y-%M-%d %H:%M:%S")))
    rows_a = None
    try:
        rows_a = json.loads(requests.get(f'{first_backend}/cart-product-table/{timestamp}').text)
    except:
        print("server unreachable")

    if rows_a is not None:
        for row_a in rows_a:
            row_b = json.loads(requests.get(f'{second_backend}/cart/{row_a["id_cart"]}/product/{row_a["id_product"]}').text)
            if row_b is None:
                # if not present, insert it
                row_a['operation'] = 'add'
                res = requests.post(f'{second_backend}/cart/{row_a["id_cart"]}/product/{row_a["id_product"]}',
                                    headers=headers, data=json.dumps(row_a))
            if row_b is not None:
                last_update_a = datetime.strptime(row_a['last_update'], '%Y-%m-%dT%H:%M:%S.%f').timestamp()
                last_update_b = datetime.strptime(row_b['last_update'], '%Y-%m-%dT%H:%M:%S.%f').timestamp()
                if last_update_a != last_update_b:
                    if last_update_a > last_update_b:
                        res = requests.put(f'{second_backend}/cart/{row_a["id_cart"]}/product/{row_a["id_product"]}',
                                            headers=headers, data=json.dumps(row_a))
                    elif last_update_a < last_update_b:
                        res = requests.put(f'{first_backend}/cart/{row_b["id_cart"]}/product/{row_b["id_product"]}',
                                            headers=headers, data=json.dumps(row_b))



                # if present, it overwrites the one with the oldest timestamp

    # second_db = requests.get(f'{second_backend}/cart-product-table/{timestamp}')
    # rows_b = json.loads(second_db.text)
    # print(rows_b)

    # if rows_a is None and rows_b is None:
    #     print("break")
    #
    # elif rows_a is not None and rows_b is None:
    #     for element in rows_a:
    #         element['operation'] ='add'
    #         api_requests.insert_cart_product(second_backend, element['id_cart'], element['id_product'], element)
    #
    # elif rows_b is not None and rows_a is None:
    #     for element in rows_b:
    #         element['operation'] ='add'
    #         api_requests.insert_cart_product(first_backend, element['id_cart'], element['id_product'], element)
    #
    # elif rows_a is not None and rows_b is not None:
    #     for row_a in rows_a:
    #         if rows_a[]
    #         for row_b in rows_b:
    #             last_update_a = row_a['last_update']
    #             last_update_b = row_b['last_update']
    #             if last_update_a > last_update_b:
    #                 break
