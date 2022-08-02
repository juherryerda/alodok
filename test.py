
from flask import Flask, request, abort, send_from_directory, make_response, Response, jsonify
from flask_cors import CORS

from waitress import serve
from datetime import datetime, timedelta

from flask_httpauth import HTTPBasicAuth,HTTPTokenAuth

import base64
import os


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

products = [
    {
        "id": 1,
        "tittle": "product 1",
        "picture_tumb": "https://picsum.photos/id/1/200/300",
        "price": "$40"
    },
    {
        "id": 2,
        "tittle": "product 2",
        "picture_tumb": "https://picsum.photos/id/2/200/300",
        "price": "$50"
    }
]

carts = {}
login = {}

@app.route('/')
@token_auth.login_required
def index():
    return "Hello, World!"


@basic_auth.verify_password
def verify_password(username, password):
    
    return username
    #user = User.query.filter_by(username=username).first()
    #if user and user.check_password(password):
    #    return user

@basic_auth.error_handler
def basic_auth_error(status):
    return (str(status))

@token_auth.verify_token
def verify_token(token):
    if(token in login and login[token] >  datetime.utcnow()):
        return True
    else:
        return False

@token_auth.error_handler
def token_auth_error(status):
    return (str(status))

@app.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    global login

    
    
    token = base64.b64encode(os.urandom(24)).decode('utf-8')
    token_expiration = datetime.utcnow() + timedelta(seconds=100)
    
    login[token] = token_expiration

    print (login)
    return ({'token': token})



@app.route('/api/v1/cart/detail/<userid>', methods=['GET'])
@token_auth.login_required
def cartdetail(userid):
    result = {
        "status": "success",
        "data": {
            "products": carts[userid]
        }
    }
    return result


@app.route('/api/v1/cart/checkout', methods=['POST'])
@token_auth.login_required
def checkout():
    return {
        "status": "success",
        "message": "Successfully checkout."
    }


@app.route('/api/v1/add_to_cart', methods=['POST'])
@token_auth.login_required
def add_to_cart():
    global carts
    body = request.json

    if str(body["user_id"]) in carts:
        temp = carts[str(body["user_id"])]
        temp.append({"title": body['product_id'], "id": "",
                    "price": "", "qty": "", "picture_thumb": ""})
        carts[str(body["user_id"])] = temp
    else:
        carts[str(body["user_id"])] = [
            {"title": body['product_id'], "id":"", "price":"", "qty":"", "picture_thumb":""}]

    print(carts)
    return {
        "status": 'success',
        "message": 'Successfully add a product to cart.'
    }


@app.route('/api/v1/detail/<id>', methods=['GET'])
@token_auth.login_required
def detail(id):
    result = {
        "status": "success",
        "data": {
            "products": list(filter(lambda x: str(x["id"]) == id, products))
        }
    }
    return result


@app.route('/api/v1/lists', methods=['GET'])
@token_auth.login_required
def lists():
    #

    result = {
        "status": "success",
        "data": {
            "products": products
        }
    }
    return result


if __name__ == '__main__':
    # app.run(host='0.0.0.0',port='7001')
    serve(app, host='0.0.0.0', port=7001)
