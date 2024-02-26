#!/usr/bin/python3
"""New view for State objects that handles all default RESTFul API actions."""

from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from api.v1.views import app_views
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """
    Retrieve a cities object.

    Args:
        state_id (str): The UUID4 string representing a State object.

    Returns:
        JSON response: A JSON response containing a cities object.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = state.cities
    list_cities = []
    for city in cities:
        list_cities.append(city.to_dict())
    return jsonify(list_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
    Retrieve a city object.

    Args:
        city_id (str): The UUID4 string representing a State object.

    Returns:
        JSON response: A JSON response containing a city object.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """
    Delete a city object.

    Args:
        city_id (str): The UUID4 string representing a city object.

    Returns:
        JSON response: An empty JSON response.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states/<state_id>/cities",
                 methods=["POST"], strict_slashes=False)
def post_city(state_id):
    """
    Create a city object.

    Returns:
        JSON response: A JSON response containing a new city object.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    try:
        new_obj = request.get_json(force=True)
    except:
        abort(400, {"Not a JSON"})
    if "name" not in new_obj:
        abort(400, {"Missing name"})
    city = City(**new_obj)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route("/cities/<city_id>",
                 methods=["PUT"], strict_slashes=False)
def put_city(city_id):
    """
    Update a city object.

    Args:
        city_id (str): The UUID4 string representing a city object.

    Returns:
        JSON response: A JSON response containing an updated city object.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    try:
        update_data = request.get_json(force=True)
    except:
        abort(400, {"Not a JSON"})
    for key, value in update_data.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict())


if __name__ == "__main__":
    pass
