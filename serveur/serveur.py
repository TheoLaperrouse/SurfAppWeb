from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
import surfAPI
import json
app = Flask(__name__)
api = Api(app)

CORS(app)


@app.route("/")
def spots():
    fichierSpots = open('serveur/spots.json', 'r')
    data = json.load(fichierSpots)
    return data


if __name__ == '__main__':
    app.run(port=5002)
