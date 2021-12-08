from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin
from utility import APP_VARIABLES
from api_requests import cart_api, product_api, cart_product_api, country_api

first_backend = APP_VARIABLES.BE_A_URL
second_backend = APP_VARIABLES.BE_B_URL
app = Flask(__name__)
api = Api(app)
CORS(app, support_credentials=True)

from multiprocessing.pool import ThreadPool

pool = ThreadPool(processes=1)


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
        return_val = cart_api.insert_cart(first_backend)
        if return_val[1] == 500:
            return_val = cart_api.insert_cart(second_backend)
        return return_val


class Cart(Resource):
    def get(self, cart_id):
        ret = cart_api.get_cart(first_backend, cart_id)
        if ret[1] == 500:
            ret = cart_api.get_cart(second_backend, cart_id)
        return ret

    def delete(self, cart_id):
        pool.apply_async(cart_api.delete_cart, (first_backend, cart_id))
        pool.apply_async(cart_api.delete_cart, (second_backend, cart_id))


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

        async_result = pool.apply_async(product_api.insert_product, (first_backend, body))
        return_val = async_result.get()

        if return_val[1] == 500:
            async_result = pool.apply_async(product_api.insert_product, (second_backend, body))
            return_val = async_result.get()

        return return_val


class Product(Resource):
    def get(self, product_id):
        ret = product_api.get_product(first_backend, product_id)
        if ret[1] == 500:
            ret = product_api.get_product(second_backend, product_id)
        return ret

    def delete(self, product_id):
        pool.apply_async(product_api.delete_product, (first_backend, product_id))
        pool.apply_async(product_api.delete_product, (second_backend, product_id))


class ListProducts(Resource):
    def get(self):
        ret = product_api.list_products(first_backend)
        if ret[1] == 500:
            ret = product_api.list_products(second_backend)
        return ret


class ListProductsByCart(Resource):
    def get(self, cart_id):
        ret = product_api.list_products_by_cart(first_backend, cart_id)
        if ret[1] == 500:
            ret = product_api.list_products_by_cart(second_backend, cart_id)
        return ret


class CartProduct(Resource):
    def get(self, cart_id, product_id):
        ret = cart_product_api.get_cart_product(first_backend, cart_id, product_id)
        if ret[1] == 500:
            ret = cart_product_api.get_cart_product(second_backend, cart_id, product_id)
        return ret

    def post(self, cart_id, product_id):
        if request.is_json:
            body = request.get_json()
        else:
            print("1")
            return None, 400
        if not body:
            print("2")
            return None, 400

        async_result = pool.apply_async(cart_product_api.post_cart_product, (first_backend, cart_id, product_id, body))
        return_val = async_result.get()

        if return_val[1] == 500:
            async_result = pool.apply_async(cart_product_api.post_cart_product,
                                            (second_backend, cart_id, product_id, body))
            return_val = async_result.get()
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
        pool.apply_async(cart_product_api.delete_cart_product, (first_backend, cart_id, product_id))
        pool.apply_async(cart_product_api.delete_cart_product, (second_backend, cart_id, product_id))


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
