#!/usr/bin/python3
"""New view for Amenity objects that handles
all default RESTFul API actions."""

from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route("/amenities",
                 methods=["GET"], strict_slashes=False)
def get_amenities():
    """
    Retrieve the list of all Amenity objects.

    Returns:
        JSON response: A JSON response containing
        a list of all Amenity objects.
    """
    amenities = storage.all(Amenity)
    list_amenities = []
    for amenity in amenities.values():
        list_amenities.append(amenity.to_dict())
    return jsonify(list_amenities)


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET"], strict_slashes=False)
def get_amenity(amenity_id):
    """
    Retrieve a amenity object.

    Args:
        amenity_id (str): The UUID4 string representing a amenity object.

    Returns:
        JSON response: A JSON response containing a amenity object.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Delete a amenity object.

    Args:
        amenity_id (str): The UUID4 string representing a amenity object.

    Returns:
        JSON response: An empty JSON response.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def post_amenity():
    """
    Create a amenity object.

    Returns:
        JSON response: A JSON response containing a new amenity object.
    """
    try:
        new_obj = request.get_json(force=True)
    except TypeError:
        abort(400, {"Not a JSON"})
    if "name" not in new_obj:
        abort(400, {"Missing name"})
    amenity = Amenity(**new_obj)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>",
                 methods=["PUT"], strict_slashes=False)
def put_amenity(amenity_id):
    """
    Update a amenity object.

    Args:
        amenity_id (str): The UUID4 string representing a amenity object.

    Returns:
        JSON response: A JSON response containing an updated amenity object.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    try:
        update_data = request.get_json(force=True)
    except TypeError:
        abort(400, {"Not a JSON"})
    for key, value in update_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict())


if __name__ == "__main__":
    pass
