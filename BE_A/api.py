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
    def get(self, productId):
        product = databaseAPI.get_product_by_id(productId)
        if not product:
            return None, 404
        return product

    def delete(self, productId):
        ret = databaseAPI.delete_product(productId)
        if not ret:
            return None, 404


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
    def get(self, cartId):
        print(cartId)
        if not isinstance(cartId, int):
            return None, 400
        cart = databaseAPI.get_cart(cartId)
        if not cart:
            return None, 404
        return cart

    def delete(self, cartId):
        ret = databaseAPI.remove_cart_products(cartId)
        if not ret:
            return None, 404


class CartProductTable(Resource):
    def get(self, timestamp):
        cartProduct = databaseAPI.get_cart_product_table(timestamp)
        if not cartProduct:
            return None, 404
        return cartProduct


class CartProduct(Resource):
    def get(self, cartId, productId):
        cartProduct = databaseAPI.get_cart_product(cartId, productId)
        if not cartProduct:
            return None, 404
        print(cartProduct)
        return cartProduct

    def put(self, cartId, productId):
        if not isinstance(cartId, int):
            return None, 400
        if not isinstance(productId, int):
            return None, 400
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

        databaseAPI.overwrite_cart_product(idCart=cartId, idProduct=productId, body=body)


    def post(self, cartId, productId):
        if not isinstance(cartId, int):
            return None, 400
        if not isinstance(productId, int):
            return None, 400
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
                databaseAPI.update_cart(newItem=True, delete=False, operation="+", idCart=cartId, idProduct=productId,
                                        body=body)
                databaseAPI.get_cart(cartId)
                print("5")
                return None, 201
            if duplicate is not None:
                databaseAPI.update_cart_product(operation="+", idCart=cartId, idProduct=productId, body=body)
                databaseAPI.update_cart(newItem=False, delete=False, operation="+", idCart=cartId, idProduct=productId,
                                        body=body)
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
                    databaseAPI.update_cart(newItem=False, delete=True, operation="-", idCart=cartId,
                                            idProduct=productId, body=body)
                    databaseAPI.remove_cart_product(idCart=cartId, idProduct=productId)
                else:
                    databaseAPI.update_cart_product(operation="-", idCart=cartId, idProduct=productId, body=body)
                    databaseAPI.update_cart(newItem=False, delete=False, operation="-", idCart=cartId,
                                            idProduct=productId, body=body)

    def delete(self, cartId, productId):
        if not isinstance(cartId, int):
            return None, 400
        if not isinstance(productId, int):
            return None, 400
        cart_product = databaseAPI.get_cart_product(idCart=cartId, idProduct=productId)
        databaseAPI.update_cart(newItem=False, delete=True, operation="-", idCart=cartId, idProduct=productId,
                                body=cart_product)
        ret = databaseAPI.remove_cart_product(cartId, productId)
        if not ret:
            return None, 404


class ListCountries(Resource):
    def get(self):
        countries = databaseAPI.list_countries()
        if not countries:
            return None, 404
        return countries


class ListSubCountries(Resource):
    def get(self, countryCode):
        subCountries = databaseAPI.list_subCountries(countryCode)
        if not subCountries:
            return None, 404
        return subCountries


api.add_resource(NewProduct, f"{basePath}/product")
api.add_resource(Product, f"{basePath}/product/<int:productId>")
api.add_resource(ListProducts, f"{basePath}/list-products")
api.add_resource(ListProductsByCart, f"{basePath}/list-products-by-cart/<int:cartId>")

api.add_resource(NewCart, f"{basePath}/cart")
api.add_resource(Cart, f"{basePath}/cart/<int:cartId>")

api.add_resource(CartProduct, f"{basePath}/cart/<int:cartId>/product/<int:productId>")

api.add_resource(CartProductTable, f"{basePath}/cart-product-table/<string:timestamp>")

api.add_resource(ListCountries, f"{basePath}/list-countries")
api.add_resource(ListSubCountries, f"{basePath}/list-subcountries/<string:countryCode>")

# api.add_resource(Shipping, f"{basePath}/shipping")
if __name__ == "__main__":
    app.run(host=APP_VARIABLES.IP, port=APP_VARIABLES.PORT, debug=True)
