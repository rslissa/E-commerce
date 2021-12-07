from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin
from utility import APP_VARIABLES
from api_requests import cart_api

first_backend = APP_VARIABLES.BE_A_URL
second_backend = APP_VARIABLES.BE_B_URL
sincronized = True
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


class Cart(Resource):
    def get(self, cartId):
        ret = cart_api.get_cart(first_backend, cartId)
        if ret[1] == 500:
            ret = cart_api.get_cart(second_backend, cartId)
        return ret


class NewProduct(Resource):
    def post(self):
        global sincronized
        if request.is_json:
            body = request.get_json()
        else:
            print("1")
            return None, 400
        if not body:
            print("2")
            return None, 400

        async_result = pool.apply_async(cart_api.insert_product, (first_backend, body))

        return_val = async_result.get()
        print(f"return val {return_val}")
        # ret = api_requests.insert_product(first_backend, body)
        if return_val[1] == 201:
            async_result = pool.apply_async(cart_api.insert_product, (second_backend, body))

            second_return_val = async_result.get()
            # second_ret = api_requests.insert_product(second_backend, body)
            if second_return_val[1] != 201:
                sincronized = False
            print(f"first backend {first_backend}")
            print(f"second backend {second_backend}")
            print(f"sincronized flag {sincronized}")
            return return_val
        elif return_val[1] == 500:
            switchBackend()
            async_result = pool.apply_async(cart_api.insert_product, (first_backend, body))
            second_return_val = async_result.get()
            if second_return_val[1] == 201:
                sincronized = False
            print(f"first backend {first_backend}")
            print(f"second backend {second_backend}")
            print(f"sincronized flag {sincronized}")
            return return_val



api.add_resource(NewProduct, f"{basePath}/product")
# api.add_resource(Product, f"{basePath}/product/<int:productId>")
# api.add_resource(ListProducts, f"{basePath}/list-products")
# api.add_resource(ListProductsByCart, f"{basePath}/list-products-by-cart/<int:cartId>")

api.add_resource(Cart, f"{basePath}/cart/<int:cartId>")

if __name__ == "__main__":
    app.run(host=APP_VARIABLES.BRIDGE_HOST, port=APP_VARIABLES.BRIDGE_PORT, debug=True)
