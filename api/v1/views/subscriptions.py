#!/usr/bin/env python3
"""the `subscriptions` module
contains the rotues to the model `Subscription`"""

from flask_login import LoginManager, login_required
from flask import jsonify, request
from api.v1.views import pen_ody
from models import storage_engine
from models.subscription import Subscription


login_manager = LoginManager()
login_manager.init_app(pen_ody)

@pen_ody.route("/subscriptions/<string:sub_id>")
@login_required
def get_subscription(sub_id):
    """returns the subscriptions data"""
    sub = storage_engine.get(model="Subscription", id=sub_id)
    if sub:
        return jsonify(sub.to_json())
    return jsonify({"error": "subscription not found"}), 404

@pen_ody.route("/subcriptions", methods=["POST"], strict_slashes=False)
@login_required
def create_subscription():
    """creates a new `Subscription` object"""
    subscriber_id = request.json.get("subscriber_id")
    writer_id = request.json.get("writer_id")
    
    if not subscriber_id or not writer_id:
        return jsonify({"error": "subscriber_id and writer_id is required"})

    sub = Subscription()    
    sub.subscriber_id = subscriber_id
    sub.writer_id = writer_id
    sub.save()
    return jsonify({"success": sub.id}), 201

@pen_ody.route("/subcriptions/<string:sub_id>", methods=["DELETE"], strict_slashes=False)
@login_required
def delete_subscription(sub_id):
    """deletes the subscription object with the given id"""
    subscription = storage_engine.get(model="Subscription", id=sub_id)
    if subscription:
        subscription.delete()
        return jsonify({"success": "subscription deleted"})
    return jsonify({"error": "subscription not found"}), 404