from flask import Flask, request, Response, jsonify, make_response
import numpy as np
import cv2
import projekt
import json
from dataclasses_serialization.json import JSONSerializer
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

migrate = Migrate(compare_type=True)
app = Flask(__name__)
# app.config.from_object(os.environ['APP_SETTINGS'])
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate.init_app(app)


@app.route('/register', methods=["POST"])
def register():
    payload = request.json
    email = payload.get('email')
    api_key = payload.get('api_key')
    api_key_hash = generate_password_hash(api_key)
    url_api_key = payload.get('url_api_key')
    url_api_key_hash = generate_password_hash(url_api_key)
    password = payload.get('password')
    password_hash = generate_password_hash(password)
    user = User(email=email, api_key=api_key_hash,
                url_api_key=url_api_key_hash, password=password_hash)
    db.session.add(user)
    db.session.commit()
    token = ''  # todo
    return jsonify({'token': token})


@app.route('/sign_in', methods=["GET", "POST"])
def sign_in():
    username_entered = request.args.get('email')
    password_entered = request.args.get('password')
    user = User.query.get(email)
    if user is not None and check_password_hash(user.password, password_entered):
        return jsonify({'token': ''})
    return jsonify({'message': 'invalid credentials'}), 401


@app.route('/api/test', methods=['POST'])
@cross_origin()
def test():
    # convert string of image data to uint8
    photo = request.files['photo'].read()
    nparr = np.fromstring(photo, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

    # do processing here....
    res = projekt.main(img)
    print(res)
    js = []

    for i in res:
        js.append(JSONSerializer.serialize(i))
    # build a response dict to send back to client
    return Response(json.dumps(js, ensure_ascii=False).encode('utf8'),  mimetype='application/json')


@app.route('/api/sum', methods=['POST'])
@cross_origin()
def test2():
    category_dict = request.json

    api_key = request.args.get('key')
    print(api_key)

    # do processing here....
    projekt.sum_by_categories(api_key, category_dict)

    return jsonify(success=True)


@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"


# start flask app
if __name__ == '__main__':
    cors = CORS(app)
    app.config.from_pyfile('config.py')
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.run(threaded=True, host="0.0.0.0", port=5000, debug=True)
