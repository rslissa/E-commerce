from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from database.databaseAPI import DatabaseAPI
from flask_cors import CORS, cross_origin
from utility import APP_VARIABLES


app = Flask(__name__)
api = Api(app)
CORS(app, support_credentials=True)


@app.route("/login")
@cross_origin(supports_credentials=True)
def login():
    return jsonify({'success': 'ok'})


basePath = APP_VARIABLES.BASEPATH
databaseAPI = DatabaseAPI()


class NewProduct(Resource):
    def post(self):
        body = request.get_json()
        if request.is_json:
            body = request.get_json()
        else:
            print("1")
            return None, 400
        if not body:
            print("2")
            return None, 400

        databaseAPI.insert_product(**body)
        print("5")
        return None, 201


class Product(Resource):
    def get(self, product_id):
        product = databaseAPI.get_product_by_id(product_id)
        if not product:
            return None, 404
        return product

    def delete(self, product_id):
        ret = databaseAPI.delete_product(product_id)
        if not ret:
            return None, 404


class ListProducts(Resource):
    def get(self):
        products = databaseAPI.list_products()
        if not products:
            return None, 404
        return products


class ListProductsByCart(Resource):
    def get(self, cart_id):
        products = databaseAPI.list_products_by_cart(cart_id)
        return products


class NewCart(Resource):
    def get(self):
        carts = databaseAPI.list_carts()
        if not carts:
            return None, 404
        return carts

    def post(self):
        cart = databaseAPI.create_cart()
        print(cart)
        if not cart:
            return None, 404
        return cart


class Cart(Resource):
    def get(self, cart_id):
        if not isinstance(cart_id, int):
            return None, 400
        cart = databaseAPI.get_cart(cart_id)
        if not cart:
            return None, 404
        return cart

    def post(self, cart_id):
        if request.is_json:
            body = request.get_json()
        else:
            print("1")
            return None, 400
        if not body:
            print("2")
            return None, 400
        databaseAPI.insert_cart_by_id(cart_id, body)

    def delete(self, cart_id):
        ret = databaseAPI.remove_cart_products(cart_id)
        if not ret:
            return None, 404


class cartTable(Resource):
    def get(self, timestamp):
        cart = databaseAPI.get_cart_table(timestamp)
        if not cart:
            return None, 404
        return cart


class cart_productTable(Resource):
    def get(self, timestamp):
        print(timestamp)
        cart_product = databaseAPI.get_cart_product_table(timestamp)
        if not cart_product:
            return None, 404
        return cart_product


class cart_product(Resource):
    def get(self, cart_id, product_id):
        cart_product = databaseAPI.get_cart_product(cart_id, product_id)
        if not cart_product or cart_product['deleted'] is True:
            return None, 404
        return cart_product

    def put(self, cart_id, product_id):
        if not isinstance(cart_id, int):
            return None, 400
        if not isinstance(product_id, int):
            return None, 400
        if request.is_json:
            body = request.get_json()
        else:
            print("1")
            return None, 400
        if not body:
            print("2")
            return None, 400
        cart = databaseAPI.get_cart(cart_id)
        if not cart:
            print("3")
            return None, 404
        product = databaseAPI.get_product_by_id(product_id)
        if not product:
            print("4")
            return None, 404
        databaseAPI.overwrite_cart_product(cart_id=cart_id, product_id=product_id, body=body)

    def post(self, cart_id, product_id):
        if not isinstance(cart_id, int):
            return None, 400
        if not isinstance(product_id, int):
            return None, 400
        if request.is_json:
            body = request.get_json()
        else:
            print("1")
            return None, 400
        if not body:
            print("2")
            return None, 400
        cart = databaseAPI.get_cart(cart_id)
        if not cart:
            print("3")
            return None, 404
        product = databaseAPI.get_product_by_id(product_id)
        if not product:
            print("4")
            return None, 404
        duplicate = databaseAPI.get_cart_product(cart_id, product_id)
        if body['operation'] == 'add':
            if duplicate is None:
                databaseAPI.insert_cart_product(cart_id, product_id, **body)
                databaseAPI.update_cart(new_item=True, delete=False, operation="+", cart_id=cart_id,
                                        product_id=product_id, body=body)
                return None, 201
            if duplicate is not None and duplicate['deleted'] is True:
                databaseAPI.delete_cart_product(cart_id, product_id)
                databaseAPI.insert_cart_product(cart_id, product_id, **body)
                databaseAPI.update_cart(new_item=True, delete=False, operation="+", cart_id=cart_id,
                                        product_id=product_id, body=body)
                return None, 201
            if duplicate is not None and duplicate['deleted'] is False:
                databaseAPI.update_cart_product(operation="+", cart_id=cart_id, product_id=product_id, body=body)
                databaseAPI.update_cart(new_item=False, delete=False, operation="+", cart_id=cart_id,
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
                    databaseAPI.update_cart(new_item=False, delete=True, operation="-", cart_id=cart_id,
                                            product_id=product_id, body=body)
                    databaseAPI.remove_cart_product(cart_id=cart_id, product_id=product_id)
                else:
                    databaseAPI.update_cart_product(operation="-", cart_id=cart_id, product_id=product_id, body=body)
                    databaseAPI.update_cart(new_item=False, delete=False, operation="-", cart_id=cart_id,
                                            product_id=product_id, body=body)

    def delete(self, cart_id, product_id):
        if not isinstance(cart_id, int):
            return None, 400
        if not isinstance(product_id, int):
            return None, 400
        cart_product = databaseAPI.get_cart_product(cart_id=cart_id, product_id=product_id)
        print(cart_product)
        if cart_product is None:
            return None, 404
        if cart_product['deleted']:
            ret = databaseAPI.delete_cart_product(cart_id, product_id)
            return ret, 200
        else:
            databaseAPI.update_cart(new_item=False, delete=True, operation="-", cart_id=cart_id, product_id=product_id,
                                    body=cart_product)
            ret = databaseAPI.remove_cart_product(cart_id, product_id)

        return ret, 200

class ListCountries(Resource):
    def get(self):
        countries = databaseAPI.list_countries()
        if not countries:
            return None, 404
        return countries


class ListSubCountries(Resource):
    def get(self, countryCode):
        subCountries = databaseAPI.list_sub_countries(countryCode)
        if not subCountries:
            return None, 404
        return subCountries


class Disponibility(Resource):
    def get(self):
        return 'ok', 200


api.add_resource(Disponibility, f"{basePath}")

api.add_resource(NewProduct, f"{basePath}/product")
api.add_resource(Product, f"{basePath}/product/<int:product_id>")
api.add_resource(ListProducts, f"{basePath}/list-products")
api.add_resource(ListProductsByCart, f"{basePath}/list-products-by-cart/<int:cart_id>")

api.add_resource(NewCart, f"{basePath}/cart")
api.add_resource(Cart, f"{basePath}/cart/<int:cart_id>")

api.add_resource(cart_product, f"{basePath}/cart/<int:cart_id>/product/<int:product_id>")

api.add_resource(cartTable, f"{basePath}/cart-table/<string:timestamp>")
api.add_resource(cart_productTable, f"{basePath}/cart-product-table/<string:timestamp>")

api.add_resource(ListCountries, f"{basePath}/list-countries")
api.add_resource(ListSubCountries, f"{basePath}/list-subcountries/<string:countryCode>")

# api.add_resource(Shipping, f"{basePath}/shipping")
if __name__ == "__main__":
    app.run(host=APP_VARIABLES.IP, port=APP_VARIABLES.PORT, debug=True)
