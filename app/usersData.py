from app import app
from config import client, DB_NAME
from bson.json_util import dumps
from flask import request, jsonify
import json
import sys
import ast
from bson import ObjectId


# Select the database
db = client[DB_NAME]
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
        # Error while trying to Update the resource
        # Add message for debugging purpose
        return "Error while Updating the User", 500

@app.route("/api/v1/delete/<user_id>", methods=['POST'])
def delete_user(user_id):
    """
       Function to remove the user.
       """
    try:
        # Delete the user
        delete_user = collection.delete_one({"_id" : ObjectId(str(user_id))})

        if delete_user.deleted_count > 0 :
            # Prepare the response
            return jsonify({"message":"Deleted Successfully"}), 202
        else:
            # Resource Not found
            return "User Not Found", 404
    except:
        # Error while trying to delete the resource
        # Add message for debugging purpose
        return "", 500

@app.route("/api/v1/find/<user_id>", methods=['GET'])
def find_user(user_id):
    """Creating a New User"""
    # Message to the user
    try:
    # Finding User
        resp = collection.find(
        {"_id" : ObjectId(str(user_id))}
        )
        result = {
            "user_id":user_id,
            "username":resp[0]["username"],
            "password":resp[0]["password"]
            }
        # Returning the object
        return jsonify(result), 201
    except:
        # Error while trying to find the resource
        # Add message for debugging purpose
        return "Error while Finding the User the User", 500
    
@app.errorhandler(404)
def page_not_found(e):
    """Send message to the user with notFound 404 status."""
    # Message to the user
    message = {
        "err":
            {
                "msg": "This route is currently not supported. Please refer API documentation."
            }
    }
    # Making the message looks good
    resp = jsonify(message)
    # Sending OK response
    resp.status_code = 404
    # Returning the object
    return resp