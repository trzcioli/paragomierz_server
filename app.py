from flask import Flask, request, Response, jsonify, make_response
import numpy as np
import cv2
import projekt
import json
from dataclasses_serialization.json import JSONSerializer

app = Flask(__name__)


@app.route('/api/test', methods=['POST'])
def test():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
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


@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"


# start flask app
if __name__ == '__main__':
    app.run(threaded=True, port=5000)
