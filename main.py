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

client = pymongo.MongoClient("localhost", 27017)
db = client.restfulapi
user_collection = db.users


def create_app(config=None):
    app = Flask(__name__)

    app.config.update(dict(DEBUG=True))
    app.config.update(config or {})

    CORS(app)

    @app.route("/")
    def hello_world():
        return "Hello World"

    @app.route("/add_user", methods=["POST"])
    def add_user():
        try:
            try:
                body = ast.literal_eval(json.dumps(request.get_json()))
            except:
                return "", 400
            record_created = user_collection.insert(body)
            if isinstance(record_created, list):
                return jsonify([str(v) for v in record_created]), 201
            else:
                return jsonify(str(record_created)), 201
        except:
            return "", 500

    @app.route("/get_user/<user_name>", methods=['GET'])
    def get_user(user_name):
        try:
            records_fetched = user_collection.find_one({ "name": user_name })
            if records_fetched != None:
                return dumps(records_fetched)
            else:
                return "User not found", 404
        except:
            return "", 500

    return app


# if __name__ == "__main__":
port = int(os.environ.get("PORT", 8000))
app = create_app()
app.run(host="0.0.0.0", port=port)
