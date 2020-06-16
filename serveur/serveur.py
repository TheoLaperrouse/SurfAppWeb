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


@app.route("/bestsRide")
def bestsRide():
    pointGeo = request.args.get('pointGeo', None)
    nomSpot = request.args.get('spotName', None)
    directionVent = request.args.get('directionVent', None)
    return surfAPI.serverResponse(pointGeo, nomSpot, directionVent)


if __name__ == '__main__':
    app.run(port=5002)
