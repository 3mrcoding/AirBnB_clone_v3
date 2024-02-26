#!/usr/bin/python3
"""New view for User objects that handles
all default RESTFul API actions."""

from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieve the list of all user objects.

    Returns:
        JSON response: A JSON response containing a list of all user objects.
    """
    users = storage.all(User)
    list_users = []
    for user in users.values():
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
    Retrieve a user object.

    Args:
        user_id (str): The UUID4 string representing a user object.

    Returns:
        JSON response: A JSON response containing a user object.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """
    Delete a user object.

    Args:
        user_id (str): The UUID4 string representing a user object.

    Returns:
        JSON response: An empty JSON response.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """
    Create a user object.

    Returns:
        JSON response: A JSON response containing a new user object.
    """
    try:
        new_user = request.get_json(force=True)
    except:
        abort(400, 'Not a JSON')
    if 'name' not in new_user:
        abort(400, 'Missing name')
    if 'email' not in new_user:
        abort(400, 'Missing email')
    if 'password' not in new_user:
        abort(400, 'Missing password')
    user = User(**new_user)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route("/users/<user_id>",
                 methods=["PUT"], strict_slashes=False)
def put_user(user_id):
    """
    Update a user object.

    Args:
        user_id (str): The UUID4 string representing a user object.

    Returns:
        JSON response: A JSON response containing an updated user object.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    try:
        update_data = request.get_json(force=True)
    except:
        abort(400, {"Not a JSON"})
    for key, value in update_data.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())


if __name__ == "__main__":
    pass
