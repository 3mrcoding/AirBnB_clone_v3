#!/usr/bin/python3
""" state api restful"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request, make_response


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """
    Retrieve the list of all State objects.

    Returns:
        JSON response: A JSON response containing a list of all State objects.
    """
    states = storage.all(State)
    list_states = []
    for state in states.values():
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_id(state_id):
    """
    Retrieve a State object.

    Args:
        state_id (str): The UUID4 string representing a State object.

    Returns:
        JSON response: A JSON response containing a State object.
    """
    stat_obj = storage.get(State, state_id)
    if stat_obj is None:
        abort(404)
    return jsonify(stat_obj.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Delete a State object.

    Args:
        state_id (str): The UUID4 string representing a State object.

    Returns:
        JSON response: An empty JSON response.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def post_state():
    """
    Create a State object.

    Returns:
        JSON response: A JSON response containing a new State object.
    """
    add = request.get_json()
    if add is None:
        abort(400, 'Not a JSON')
    if "name" not in add:
        abort(400, 'Missing name')
    stat_obj = State(name=add['name'])
    storage.new(stat_obj)
    storage.save()
    return jsonify(stat_obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """
    Update a State object.

    Args:
        state_id (str): The UUID4 string representing a State object.

    Returns:
        JSON response: A JSON response containing an updated State object.
    """
    add = request.get_json()
    stat_obj = storage.get(State, state_id)
    if not stat_obj:
        abort(404)
    if not add:
        abort(400, "Not a JSON")
    ignoreKeys = ['id', 'created_at', 'updated_at']
    for key, value in add.items():
        if key not in ignoreKeys:
            setattr(stat_obj, key, value)
    stat_obj.save()
    return jsonify(stat_obj.to_dict())

if __name__ == '__main__':
    pass
