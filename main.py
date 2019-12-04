#!/usr/bin/env python3
"""
Documentation

See also https://www.python-boilerplate.com/flask
"""
import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from bson.json_util import dumps
import pymongo
import ast
import json

client = pymongo.MongoClient("mongodb+srv://a:a@cluster0-4pu9k.mongodb.net/test?retryWrites=true&w=majority")
db = client.restfulapi
score_collection = db.scores


app = Flask(__name__)

app.config.update(dict(DEBUG=True))
app.config.update({})

CORS(app)

@app.route("/")
def hello_world():
    return "Hello World"

@app.route("/score", methods=["POST"])
def post_score():
    try:
        try:
            body = ast.literal_eval(json.dumps(request.get_json()))
        except:
            return "", 400
        records_fetched = score_collection.find_one({ "name": body["name"] })
        if records_fetched != None:
            score_collection.update_one({ "name": body["name"] }, { "$set": { "score": body["score"] } })
            return "", 201
        record_created = score_collection.insert(body)
        if isinstance(record_created, list):
            return jsonify([str(v) for v in record_created]), 201
        else:
            return jsonify(str(record_created)), 201
    except:
        return "", 500

@app.route("/score/<user_name>", methods=['GET'])
def get_score(user_name):
    try:
        records_fetched = score_collection.find_one({ "name": user_name })
        if records_fetched != None:
            return dumps(records_fetched)
        else:
            return "User not found", 404
    except:
        return "", 500


def main(a=None, b=None):
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
