#!/usr/bin/python3
"""/status route for API v1."""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity


@app_views.route('/status')
def status():
    """return status of the API as json response."""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """endpoint that retrieves the number of each objects by type"""
    all_objs = {
        "amenities": storage.count(Amenity),
        "cities":  storage.count(City),
        "places":  storage.count(Place),
        "reviews":  storage.count(Review),
        "states":  storage.count(State),
        "users":  storage.count(User)
    }
    return jsonify(all_objs)
