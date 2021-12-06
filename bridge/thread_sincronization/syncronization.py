from datetime import datetime
import time
from requests.structures import CaseInsensitiveDict
import requests
import json

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
    modified = {o : (d1[o], d2[o]) for o in shared_keys if d1[o] != d2[o]}
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

        first_db = requests.get(f'http://localhost:5001/bea/v1/cart-product-table/{timestamp}')
        rows_a = json.loads(first_db.text)
        print(rows_a)

        second_db = requests.get(f'http://localhost:5002/beb/v1/cart-product-table/{timestamp}')
        rows_b = json.loads(second_db.text)
        print(rows_b)

        if rows_a is None and rows_b is None:
            print("break")

        elif rows_a is not None and rows_b is None:
            for element in rows_a:
                print(element)
