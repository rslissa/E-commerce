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
    # def delete(self, cartId):
    #     ret = databaseAPI.delete_cart_products(cartId)
    #     ret = databaseAPI.remove_cart_product(cartId, productId)
    #     if not ret:
    #         return None, 404
    #
    #     - aggiorna cart con cartId= cartId e poni tutto a zero



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

        cart = databaseAPI.get_cart(cartId)
        if not cart:
            print("3")
            return None, 404

        product = databaseAPI.get_product_by_id(productId)
        if not product:
            print("4")
            return None, 404

        duplicate = databaseAPI.get_cart_product(cartId, productId)

        if body['operation'] == 'add':
            if duplicate is None:
                databaseAPI.insert_cart_product(cartId, productId, **body)
                databaseAPI.update_cart(newItem=True,delete=False, operation="+", idCart=cartId, idProduct=productId,body=body)
                databaseAPI.get_cart(cartId)
                print("5")
                return None, 201
            if duplicate is not None:
                databaseAPI.update_cart_product(operation="+", idCart=cartId, idProduct=productId, body=body)
                databaseAPI.update_cart(newItem=False, delete=False, operation="+", idCart=cartId,idProduct=productId, body=body)
                print("6")
                return None, 201

        if body['operation'] == 'sub':
            if duplicate is None:
                print("7")
                return None, 404

            if duplicate is not None:
                print(duplicate)
                product_quantity = duplicate['quantity']
                if product_quantity <= body['quantity']:
                    databaseAPI.update_cart(newItem=False, delete=True, operation="-", idCart=cartId,idProduct=productId, body=body)
                    databaseAPI.remove_cart_product(idCart=cartId, idProduct=productId)
                else:
                    print("sono qui")
                    databaseAPI.update_cart_product(operation="-", idCart=cartId, idProduct=productId, body=body)
                    databaseAPI.update_cart(newItem=False, delete=False, operation="-", idCart=cartId,idProduct=productId, body=body)
    def delete(self, cartId, productId ):
        cart_product = databaseAPI.get_cart_product(idCart=cartId, idProduct=productId)
        databaseAPI.update_cart(newItem=False, delete=True, operation="-", idCart=cartId, idProduct=productId,
                                body=cart_product)
        ret = databaseAPI.remove_cart_product(cartId, productId)
        if not ret:
            return None, 404




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

class ListProductsByCart(Resource):
    def get(self, cartId):
        products = databaseAPI.list_products_by_cart(cartId)
        return products


api.add_resource(Product, f"{basePath}/product/<string:name>")
api.add_resource(ListProducts, f"{basePath}/list-products")
api.add_resource(ListProductsByCart, f"{basePath}/list-products-by-cart/<int:cartId>")

api.add_resource(Cart, f"{basePath}/cart/<int:cartId>")
api.add_resource(NewCart, f"{basePath}/cart")
api.add_resource(CartProduct, f"{basePath}/cart/<int:cartId>/product/<int:productId>")

# api.add_resource(Shipping, f"{basePath}/shipping")
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
