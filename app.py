from __future__ import print_function
import cv2
import pickle
import numpy as np
import flask
import io
from PIL import Image
from load_facenet import *

app = flask.Flask(__name__)
global model, graph
model, graph = init()


@app.route("/", methods=["GET"])
def health_check():
    return flask.jsonify({"status": 200})


@app.route("/verify", methods=["POST"])
def verify():
    name = flask.request.args.get("name")
    image = flask.request.files["image"].read()
    faceCascade = cv2.CascadeClassifier('assets/haarcascade_frontalface_default.xml')
    name = str(name)
    image = Image.open(io.BytesIO(image))
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face = faceCascade.detectMultiScale(gray, 1.3, 5)
    output = {"code": -10, "message": "Start"}
    if len(face) > 0:
        for (x, y, w, h) in face:
            face = img[y:y + h, x:x + w]
            resize_img = cv2.resize(face, (96, 96))
            with graph.as_default():
                handle = open("assets/encoding2.pickle", "rb")
                database = pickle.load(handle)
                handle.close()
                img = resize_img[..., ::-1]
                img = np.around(np.transpose(img, (2, 0, 1)) / 255.0, decimals=12)
                x_train = np.array([img])
                embedding = model.predict_on_batch(x_train)
                try:
                    dist = np.linalg.norm(embedding - database[name])
                except:
                    output["code"] = -3
                    output["message"] = "Name does not exist in database"
                    return flask.jsonify(output)
                score = dist
                print("Score:-  {}".format(score))

                handle = open("assets/encoding2.pickle", "wb")
                pickle.dump(database, handle, protocol=pickle.HIGHEST_PROTOCOL)
                handle.close()
                if score <= 0.85:
                    output["code"] = 1
                    output["message"] = "Person is verified correctly"
                    output["score"] = str(score)
                    return flask.jsonify(output)
                else:
                    output["code"] = 0
                    output["message"] = "Person is not verified"
                    output["score"] = str(score)
                    return flask.jsonify(output)

            output["code"] = -2
            output["message"] = "Model could not be loaded"
            return flask.jsonify(output)
    else:
        output["code"] = -1
        output["message"] = "No frontal face detected on picture"
        return flask.jsonify(output)


@app.route("/add", methods=["POST"])
def add():
    name = flask.request.args.get("name")
    image = flask.request.files["image"].read()
    faceCascade = cv2.CascadeClassifier('assets/haarcascade_frontalface_default.xml')
    name = str(name)
    image = Image.open(io.BytesIO(image))
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face = faceCascade.detectMultiScale(gray, 1.3, 5)
    output = {"code": -10, "message": "Inside add new face"}
    if len(face) > 0:
        for (x, y, w, h) in face:
            face = img[y:y + h, x:x + w]
            resize_img = cv2.resize(face, (96, 96))
            handle = open("assets/encoding2.pickle", "rb")
            database = pickle.load(handle)
            handle.close()
            with graph.as_default():
                img = resize_img[..., ::-1]
                img = np.around(np.transpose(img, (2, 0, 1)) / 255.0, decimals=12)
                x_train = np.array([img])
                embedding = model.predict_on_batch(x_train)
                database[name] = embedding
                handle = open("assets/encoding2.pickle", "wb")
                pickle.dump(database, handle, protocol=pickle.HIGHEST_PROTOCOL)
                handle.close()
                output["code"] = 1
                output["message"] = "Face added to the database"
                return flask.jsonify(output)
    else:
        output["code"] = -1
        output["message"] = "No frontal face detected"
        return flask.jsonify(output)


if __name__ == '__main__':
    app.run(host="localhost", port="5000", debug=False)
