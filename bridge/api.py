from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin
import requests
import json

app = Flask(__name__)
api = Api(app)
CORS(app, support_credentials=True)


@app.route("/login")
@cross_origin(supports_credentials=True)
def login():
    return jsonify({'success': 'ok'})


basePath = "/bridge/v1"


class Cart(Resource):
    def get(self, cartId):
        cart = requests.get(f'http://localhost:5000/api/v1/cart/{cartId}')
        print(cart.status_code)
        if not cart:
            return None, 404
        return json.loads(cart.text)


api.add_resource(Cart, f"{basePath}/cart/<int:cartId>")

# api.add_resource(Shipping, f"{basePath}/shipping")
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
