from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """get amount of pictures"""
    if data:
        return jsonify(length=len(data)),200
    else:
        return jsonify(length=0),200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    #search for the picture with the given id
    picture = next((item for item in data if item.get("id") == id), None)
    if picture:
        return jsonify(picture),200
    else:
        return jsonify({"error": "Picture not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    # Get JSON data from request
    new_picture = request.get_json()
    # Basic validation: check required fields (e.g., "id" and "url")
    if not new_picture or "id" not in new_picture or "url" not in new_picture:
        return jsonify({"error": "Missing required picture data"}), 400
    # Optional: check if picture with same id already exists
    if any(item.get("id") == new_picture["id"] for item in data):
        return jsonify({"error": "Picture with this ID already exists"}), 409
    
    # Add the new picture to data list
    data.append(new_picture)

    # Return the new picture with status 201 Created
    return jsonify(new_picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
     # Get JSON data from request
    updated_data = request.get_json()

    # Find the picture with the given id
    picture = next((item for item in data if item.get("id") == id), None)

    if not picture:
        return jsonify({"error": "Picture not found"}), 404

    # Update the picture's fields with the new data
    # For example, update all keys present in updated_data
    for key, value in updated_data.items():
        picture[key] = value

    # Return the updated picture
    return jsonify(picture), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    # Find the index of the picture with the given id
    index = next((i for i, item in enumerate(data) if item.get("id") == id), None)
    
    if index is None:
        return jsonify({"error": "Picture not found"}), 404
    
    # Remove the picture from the list
    deleted_picture = data.pop(index)
    
    # Return a success message or the deleted picture
    return jsonify({"message": "Picture deleted", "picture": deleted_picture}), 200
