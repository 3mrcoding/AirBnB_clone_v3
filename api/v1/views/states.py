#!/usr/bin/python3
""" state api restful"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """return status of the API as json response."""
    states = storage.all(State)
    list_states = []
    for state in states.values():
        list_states.append(state.to_dict())
    return jsonify(list_states)

@app_views.route('/states/<id>', methods=['GET'], strict_slashes=False)
def states_id(id):
    """
    return status of the API as json response.
        Args:
        id (str): The UUID4 string representing a State object.

    Returns:
        JSON response: state
    """
    states = storage.all(State)
    list_states = []
    for state in states.values():
        if state.id == id:
            list_states.append(state.to_dict())
            break
        else:
            abort(404)
    return jsonify(list_states)

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
