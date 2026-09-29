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
    if data:
        return jsonify(data), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if data:
        for picture in data:
            if picture['id'] == id:
                return jsonify(picture), 200
        
        return {"message": "URL not found"}, 404

    return {"message": "Internal server error"}, 500


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    # Get the JSON data from the incoming request
    new_picture = request.get_json()

    # Check if the JSON data is empty or None
    if not new_picture:
        # Return a JSON response indicating that the request data is invalid
        # with a status code of 422 (Unprocessable Entity)
        return {"message": "Invalid input, no data provided"}, 422

    # Proceed with further processing of 'new_picture', such as adding it to a database
    # or validating its contents before saving it
    try:
        for picture in data:
            if picture['id'] == new_picture['id']:
                return {"Message": f"picture with id {picture['id']} already present"},302
    
        data.append(new_picture)
    except NameError:
        return {"message": "data not defined"}, 500
    # Assuming the processing is successful, return the picture id with status code 200
    return new_picture, 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    update_pic = request.get_json()
    try:
        for index, picture in enumerate(data):
            if picture['id'] == id:
                data[index] = update_pic
                return picture, 200
    except NameError:
        return {"message": "data not defined"}, 500
    # Assuming the processing is successful, return the picture id with status code 200
    return {"message": "picture not found"},404
######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    try:
        for picture in data:
            if picture['id'] == id:
                data.remove(picture)
                return {}, 204
    except NameError:
        return {"message": "data not defined"}, 500
    # Assuming the processing is successful, return the picture id with status code 200
    return {"message": "picture not found"},404
