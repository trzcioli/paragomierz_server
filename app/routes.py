from app import app, db
from flask import request, Response, jsonify, make_response, g
import numpy as np
import cv2
from app import receipt_image_processor
import json
from flask_cors import cross_origin
from dataclasses_serialization.json import JSONSerializer
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import auth
import requests
from cryptography.fernet import Fernet


def encrypt(message: bytes) -> bytes:
    return Fernet(app.config["SECRET_KEY"]).encrypt(message)


def decrypt(token: bytes) -> bytes:
    return Fernet(app.config["SECRET_KEY"]).decrypt(token)


@auth.verify_password
def verify_password(token, _):
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True


@app.route('/register', methods=["POST"])
def register():
    payload = request.json
    email = payload.get('email')
    api_key = payload.get('api_key')
    api_key_hash = encrypt(api_key.encode()).decode()
    print(api_key_hash)
    url_api_key = payload.get('url_api_key')
    url_api_key_hash = encrypt(url_api_key.encode()).decode()
    password = payload.get('password')
    password_hash = generate_password_hash(password)
    user = User(email=email, api_key=api_key_hash,
                url_api_key=url_api_key_hash, password=password_hash)
    db.session.add(user)
    db.session.commit()
    token = user.generate_auth_token()
    return token


@app.route('/sign_in', methods=["GET", "POST"])
def sign_in():
    payload = request.json
    email = payload.get('email')
    password = payload.get('password')
    user = User.query.get(email)
    if user is not None and check_password_hash(user.password, password):
        return user.generate_auth_token()
    return jsonify({'message': 'invalid credentials'}), 401


@app.route('/api/process-image', methods=['POST'])
@cross_origin()
@auth.login_required
def process_image():
    # convert string of image data to uint8
    photo = request.files['photo'].read()
    nparr = np.fromstring(photo, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

    # do processing here....
    res = receipt_image_processor.process_image(img)
    print(res)
    js = []

    for i in res:
        js.append(JSONSerializer.serialize(i))
    # build a response dict to send back to client
    return Response(json.dumps(js, ensure_ascii=False).encode('utf8'),  mimetype='application/json')


@app.route('/api/sum', methods=['POST'])
@cross_origin()
@auth.login_required
def sum_categories():
    key = decrypt(g.user.url_api_key.encode()).decode()
    receipt_image_processor.sum_by_categories(key, request.json)

    return jsonify(success=True)


@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"


@app.route('/api/categories', methods=['GET'])
@cross_origin()
@auth.login_required
def get_categories():
    api_key = g.user.api_key
    key = decrypt(api_key.encode()).decode()

    url = f"https://secure.kontomierz.pl/k4/categories.json?direction=withdrawal&in_wallet=true&api_key={key}"

    resp = requests.get(url)

    return resp.json()
