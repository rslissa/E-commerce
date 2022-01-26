from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin
from database.CacheAPI import DatabaseAPI
from utility import APP_VARIABLES
from api_requests import cart_api, product_api, cart_product_api, country_api
from multiprocessing.pool import ThreadPool
from threading import Thread

first_backend = APP_VARIABLES.BE_A_URL
second_backend = APP_VARIABLES.BE_B_URL
app = Flask(__name__)
api = Api(app)
CORS(app, support_credentials=True)

pool = ThreadPool(processes=1)

cache = DatabaseAPI()


def switchBackend():
    global first_backend
    global second_backend
    if first_backend == APP_VARIABLES.BE_A_URL:
        first_backend = APP_VARIABLES.BE_B_URL
        second_backend = APP_VARIABLES.BE_A_URL
    else:
        first_backend = APP_VARIABLES.BE_A_URL
        second_backend = APP_VARIABLES.BE_B_URL


@app.route("/login")
@cross_origin(supports_credentials=True)
def login():
    return jsonify({'success': 'ok'})


basePath = APP_VARIABLES.BRIDGE_BASEPATH


class NewCart(Resource):
    def post(self):
        cache.create_cart()
        Thread(target=self.thread_post_NewCart).start()

    def thread_post_NewCart(self):
        return_val = cart_api.insert_cart(first_backend)
        if return_val[1] == 500:
            return_val = cart_api.insert_cart(second_backend)
        return return_val


class Cart(Resource):
    def get(self, cart_id):
        ret = cache.get_cart(cart_id)
        # if is None means that the data is not in the cache
        if ret is None:
            ret = cart_api.get_cart(first_backend, cart_id)
            if ret[1] == 500:
                ret = cart_api.get_cart(second_backend, cart_id)
            if ret is not None and ret[1] != 500 and ret[1] != 404:
                print(f"ret server 1 {ret[0]}")
                cache.insert_cart_by_id(cart_id, ret[0])
        return ret

    def delete(self, cart_id):
        ret = cache.remove_cart_products(cart_id)
        if not ret:
            return None, 404
        Thread(target=self.thread_delete_Cart, args=(cart_id,)).start()
        return None, 200

    def thread_delete_Cart(self, cart_id):
        cart_api.delete_cart(first_backend, cart_id)
        cart_api.delete_cart(second_backend, cart_id)


class NewProduct(Resource):
    def post(self):
        if request.is_json:
            body = request.get_json()
        else:
            print("1")
            return None, 400
        if not body:
            print("2")
            return None, 400
        cache.insert_product(**body)
        Thread(target=self.thread_post_NewProduct, args=(body,)).start()

    def thread_post_NewProduct(self, body):
        return_val = product_api.insert_product(first_backend, body)
        if return_val[1] == 500:
            return_val = product_api.insert_product(second_backend, body)
        return return_val


class Product(Resource):
    def get(self, product_id):
        ret = cache.get_product_by_id(product_id)
        if ret is None:  # if is None means that the data is not in the cache
            ret = product_api.get_product(first_backend, product_id)
            if ret[1] == 500:
                ret = product_api.get_product(second_backend, product_id)
            if ret is not None and ret[1] != 500 and ret[1] != 404:
                print(f"ret server 1 {ret[0]}")
                cache.insert_product(**ret[0])
        return ret

    def delete(self, product_id):
        cache.delete_product(product_id)
        Thread(target=self.thread_delete_Product, args=(product_id,)).start()
        return None, 200

    def thread_delete_Product(self, product_id):
        product_api.delete_product(first_backend, product_id)
        product_api.delete_product(second_backend, product_id)


class ListProducts(Resource):
    def get(self):
        ret = product_api.list_products(first_backend)
        if ret[1] == 500:
            ret = product_api.list_products(second_backend)
        if ret is not None and ret[1] != 500 and ret[1] != 404:
            for e in ret[0]:
                el_cache = cache.get_product_by_id(e['id_product'])
                if el_cache is None:
                    cache.insert_product(**e)
        return ret


class ListProductsByCart(Resource):
    def get(self, cart_id):
        ret = product_api.list_products_by_cart(first_backend, cart_id)
        if ret[1] == 500:
            ret = product_api.list_products_by_cart(second_backend, cart_id)
        if ret is not None and ret[1] != 500 and ret[1] != 404:
            for e in ret[0]:
                el_cache = cache.get_product_by_id(e['id_product'])
                if el_cache is None:
                    cache.insert_product(**e)
        return ret


class CartProduct(Resource):
    def get(self, cart_id, product_id):
        ret_cart_product = cache.get_cart_product(cart_id, product_id)
        if ret_cart_product is None:  # if is None means that the data is not in the cache
            ret_cart_product = cart_product_api.get_cart_product(first_backend, cart_id, product_id)
            if ret_cart_product[1] == 500:
                ret_cart_product = cart_product_api.get_cart_product(second_backend, cart_id, product_id)
            if ret_cart_product is not None and ret_cart_product[1] != 500 and ret_cart_product[1] != 404:
                ret_cart = cache.get_cart(cart_id)
                if ret_cart is None:
                    cache.load_cart_on_cache(cart_id)
                ret_product = cache.get_product_by_id(product_id)
                if ret_product is None:
                    cache.load_product_on_cache(product_id)
                cache.insert_cart_product(cart_id, product_id, **ret_cart_product[0])
        return ret_cart_product

    def post(self, cart_id, product_id):
        if request.is_json:
            body = request.get_json()
        else:
            print("1")
            return None, 400
        if not body:
            print("2")
            return None, 400
        Thread(target=self.thread_post_CartProduct, args=(cart_id, product_id, body,)).start()
        ret_cart = cache.get_cart(cart_id)
        if ret_cart is None:
            cache.load_cart_on_cache(cart_id)
        ret_product = cache.get_product_by_id(product_id)
        if ret_product is None:
            cache.load_product_on_cache(product_id)

        duplicate = cache.get_cart_product(cart_id, product_id)
        if body['operation'] == 'add':
            if duplicate is None:
                body["deleted"] = False
                cache.insert_cart_product(cart_id, product_id, **body)
                cache.update_cart(new_item=True, delete=False, operation="+", cart_id=cart_id,
                                        product_id=product_id, body=body)
                return None, 201
            if duplicate is not None and duplicate['deleted'] is True:
                cache.delete_cart_product(cart_id, product_id)
                body["deleted"] = False
                cache.insert_cart_product(cart_id, product_id, **body)
                cache.update_cart(new_item=True, delete=False, operation="+", cart_id=cart_id,
                                        product_id=product_id, body=body)
                return None, 201
            if duplicate is not None and duplicate['deleted'] is False:
                cache.update_cart_product(operation="+", cart_id=cart_id, product_id=product_id, body=body)
                cache.update_cart(new_item=False, delete=False, operation="+", cart_id=cart_id,
                                        product_id=product_id, body=body)
                print("6")
                return None, 201

        if body['operation'] == 'sub':
            # if duplicate is None:
            #     print("7")
            #     return None, 404

            if duplicate is not None:
                print(duplicate)
                product_quantity = duplicate['quantity']
                if product_quantity <= body['quantity']:
                    cache.update_cart(new_item=False, delete=True, operation="-", cart_id=cart_id,
                                            product_id=product_id, body=body)
                    cache.remove_cart_product(cart_id=cart_id, product_id=product_id)
                else:
                    cache.update_cart_product(operation="-", cart_id=cart_id, product_id=product_id, body=body)
                    cache.update_cart(new_item=False, delete=False, operation="-", cart_id=cart_id,
                                            product_id=product_id, body=body)
        return None, 200

    def thread_post_CartProduct(self, cart_id, product_id, body):
        return_val = cart_product_api.post_cart_product(first_backend, cart_id, product_id, body)
        if return_val[1] == 500:
            return_val = cart_product_api.post_cart_product(second_backend, cart_id, product_id, body)
        return return_val

    def put(self, cart_id, product_id):
        if request.is_json:
            body = request.get_json()
        else:
            print("1")
            return None, 400
        if not body:
            print("2")
            return None, 400

        async_result = pool.apply_async(cart_product_api.put_cart_product, (first_backend, cart_id, product_id, body))
        return_val = async_result.get()

        if return_val[1] == 500:
            async_result = pool.apply_async(cart_product_api.put_cart_product,
                                            (second_backend, cart_id, product_id, body))
            return_val = async_result.get()
        return return_val

    def delete(self, cart_id, product_id):
        if not isinstance(cart_id, int):
            return None, 400
        if not isinstance(product_id, int):
            return None, 400

        Thread(target=self.thread_delete_CartProduct, args=(cart_id, product_id,)).start()

        cart_product = cache.get_cart_product(cart_id=cart_id, product_id=product_id)
        print(cart_product)
        if cart_product is None:
            return None, 404
        if cart_product['deleted']:
            ret = cache.delete_cart_product(cart_id, product_id)
            return ret, 200
        else:
            cache.update_cart(new_item=False, delete=True, operation="-", cart_id=cart_id, product_id=product_id,
                                    body=cart_product)
            ret = cache.remove_cart_product(cart_id, product_id)

        return None, 200

    def thread_delete_CartProduct(self, cart_id, product_id):
        cart_product_api.delete_cart_product(first_backend, cart_id, product_id)
        cart_product_api.delete_cart_product(second_backend, cart_id, product_id)


class ListCountries(Resource):
    def get(self):
        ret = country_api.list_countries(first_backend)
        if ret[1] == 500:
            ret = country_api.list_countries(second_backend)
        return ret


class ListSubCountries(Resource):
    def get(self, country_code):
        ret = country_api.list_sub_countries(first_backend, country_code)
        if ret[1] == 500:
            ret = country_api.list_sub_countries(second_backend, country_code)
        return ret


api.add_resource(NewProduct, f"{basePath}/product")
api.add_resource(Product, f"{basePath}/product/<int:product_id>")

api.add_resource(ListProducts, f"{basePath}/list-products")
api.add_resource(ListProductsByCart, f"{basePath}/list-products-by-cart/<int:cart_id>")

api.add_resource(NewCart, f"{basePath}/cart")
api.add_resource(Cart, f"{basePath}/cart/<int:cart_id>")

api.add_resource(CartProduct, f"{basePath}/cart/<int:cart_id>/product/<int:product_id>")

api.add_resource(ListCountries, f"{basePath}/list-countries")
api.add_resource(ListSubCountries, f"{basePath}/list-subcountries/<string:country_code>")

if __name__ == "__main__":
    app.run(host=APP_VARIABLES.BRIDGE_HOST, port=APP_VARIABLES.BRIDGE_PORT, debug=True)
