from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from database.databaseAPI import DatabaseAPI
from flask_cors import CORS, cross_origin

app = Flask(__name__)
api = Api(app)
CORS(app, support_credentials=True)


@app.route("/login")
@cross_origin(supports_credentials=True)
def login():
    return jsonify({'success': 'ok'})


basePath = "/api/v1"
databaseAPI = DatabaseAPI()


#
# class Shipping(Resource):
#     def post(self):
#         if request.is_json:
#             body = request.get_json()
#         else:
#             print("1")
#             return None, 400
#         if not body:
#             print("2")
#             return None, 400
#
#         duplicate = storeDB.get_product(name)
#
#         if duplicate is not None:
#             print("4")
#             return None, 409
#
#         storeDB.insert_product(name, **body)
#         print("5")
#         return None, 201
class NewCart(Resource):
    def get(self):
        cart = databaseAPI.create_cart()
        print(cart)
        if not cart:
            return None, 404
        return cart


class Cart(Resource):
    def get(self, cartId):
        cart = databaseAPI.get_cart(cartId)
        print(cart)
        if not cart:
            return None, 404
        return cart

    def post(self, cartId):
        if cartId != 0:
            cart = databaseAPI.get_cart(cartId)
            if not cart:
                return None, 404


class CartProduct(Resource):
    def post(self, cartId, productId):
        if request.is_json:
            body = request.get_json()
        else:
            print("1")
            return None, 400
        if not body:
            print("2")
            return None, 400

        duplicate = databaseAPI.get_cart_product(cartId, productId)

        if duplicate is not None:
            print("4")
            return None, 409

        databaseAPI.insert_cart_product(cartId, productId, **body)
        print("5")
        return None, 201


class Product(Resource):
    def get(self, name):
        product = databaseAPI.get_product(name)
        if not product:
            return None, 404
        return product

    def delete(self, name):
        ret = databaseAPI.delete_product(name)
        if not ret:
            return None, 404

    def post(self, name):
        if request.is_json:
            body = request.get_json()
        else:
            print("1")
            return None, 400
        if not body:
            print("2")
            return None, 400

        duplicate = databaseAPI.get_product(name)

        if duplicate is not None:
            print("4")
            return None, 409

        databaseAPI.insert_product(name, **body)
        print("5")
        return None, 201


class ListProducts(Resource):
    def get(self):
        products = databaseAPI.list_products()
        if not products:
            return None, 404
        return products


api.add_resource(Product, f"{basePath}/product/<string:name>")
api.add_resource(ListProducts, f"{basePath}/list-products")

api.add_resource(Cart, f"{basePath}/cart/<int:cartId>")
api.add_resource(NewCart, f"{basePath}/cart")
api.add_resource(CartProduct, f"{basePath}/cart/<int:cartId>/product/<int:productId>")

# api.add_resource(Shipping, f"{basePath}/shipping")
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
