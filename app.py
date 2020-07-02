from flask import Flask, request, Response, jsonify, make_response
import numpy as np
import cv2
import projekt
import json
from dataclasses_serialization.json import JSONSerializer
from flask_cors import CORS, cross_origin

app = Flask(__name__)


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
