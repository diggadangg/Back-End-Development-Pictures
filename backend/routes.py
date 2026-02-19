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
    """return the full list of pictures"""
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((item for item in data if item.get("id") == id), None)
    if picture:
        return jsonify(picture), 200
    else:
        return jsonify({"error": "Picture not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.get_json()

    # Only require "id" to be present
    if not new_picture or "id" not in new_picture:
        return jsonify({"error": "Missing required picture data"}), 400

    # Check for duplicate — return 302 with the exact message the tests expect
    if any(item.get("id") == new_picture["id"] for item in data):
        return jsonify({"Message": f"picture with id {new_picture['id']} already present"}), 302

    data.append(new_picture)
    return jsonify(new_picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    updated_data = request.get_json()

    picture = next((item for item in data if item.get("id") == id), None)

    if not picture:
        return jsonify({"error": "Picture not found"}), 404

    for key, value in updated_data.items():
        picture[key] = value

    return jsonify(picture), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    index = next((i for i, item in enumerate(data) if item.get("id") == id), None)

    if index is None:
        return jsonify({"error": "Picture not found"}), 404

    data.pop(index)

    # 204 No Content — no body
    return make_response("", 204)