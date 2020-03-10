from app import app
from config import client
from bson.json_util import dumps
from flask import request, jsonify
import json
import sys
import ast
from bson import ObjectId


# Select the database
db = client.UsersData
# Select the collection
collection = db.Users

@app.route("/")
def get_initial_response():
    """Welcome message for the API."""
    # Message to the user
    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'Welcome to the Flask API'
    }
    # Making the message looks good
    resp = jsonify(message)
    # Returning the object
    return resp

@app.route("/api/v1/create", methods=['POST'])
def create_user():
    """Creating a New User"""
    # Message to the user
    try:
    # Create new users
        try:
            body = request.json
        except:
            # Bad request as request body is not available
            # Add message for debugging purpose
            return "Could Not Find a body", 400
        # Making the message looks good
        resp = collection.insert(body)
        # Returning the object
        return jsonify(str(resp)), 201
    except:
        # Error while trying to create the resource
        # Add message for debugging purpose
        return "Error while Creating the User", 500

@app.route("/api/v1/update/<user_id>", methods=['POST'])
def update_user(user_id):
    """Creating a New User"""
    # Message to the user
    try:
    # Updating User
        try:
            body = request.json
        except:
            # Bad request as request body is not available
            # Add message for debugging purpose
            return "Could Not Find a body", 400
        # Making the message looks good
        resp = collection.find_one_and_update(
        {"_id" : ObjectId(str(user_id))},
        {"$set":
            body
        },upsert=True
        )
        result = {
            "user_id":user_id,
            "username":resp["username"],
            "password":resp["password"]
            }
        # Returning the object
        return jsonify(result), 201
    except:
        # Error while trying to create the resource
        # Add message for debugging purpose
        return "Error while Updating the User", 500
