#!/usr/bin/python3
"""
Create a new view for Review object that
handles all default RESTFul API actions.
"""
from os import getenv
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.amenity import Amenity

storage_type = getenv('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    """Get all Amenities."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if storage_type == 'db':
        p_amenities = place.amenities
    else:
        p_amenities = place.amenity_ids
    all_amenities = []
    for amenity in p_amenities:
        all_amenities.append(amenity.to_dict())
    return jsonify(all_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Delete amenity by id depending on storage."""
    amenity = storage.get(Amenity, amenity_id)
    place = storage.get(Place, place_id)
    if place is None or amenity is None:
        abort(404)
    if storage_type == 'db':
        p_amenities = place.amenities
    else:
        p_amenities = place.amenity_ids
    if amenity not in p_amenities:
        abort(404)
    p_amenities.remove(amenity)
    place.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def create_place_amenity(place_id, amenity_id):
    """Create amenities depending on storage."""
    amenity = storage.get(Amenity, amenity_id)
    place = storage.get(Place, place_id)
    if place is None or amenity is None:
        abort(404)
    if storage_type == 'db':
        p_amenities = place.amenities
    else:
        p_amenities = place.amenity_ids
    if amenity in p_amenities:
        return jsonify(amenity.to_dict())
    p_amenities.append(amenity)
    place.save()
    return make_response(jsonify(amenity.to_dict()), 201)
