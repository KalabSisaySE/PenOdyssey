#!/usr/bin/env python3
"""the `likes` module
contains the routes for the `Like` model
"""

from flask_login import LoginManager, login_required
from flask import jsonify, request
from api.v1.views import pen_ody
from models import storage_engine
from models.like import Like

login_manager = LoginManager()
login_manager.init_app(pen_ody)


@pen_ody.route("likes/<string:like_id>", strict_slashes=False)
@login_required
def get_like(like_id):
    """returns the like data"""
    like = storage_engine.get(model="Like", id=like_id)
    if like:
        return jsonify(like.to_json())
    return jsonify({"error": "like not found"}), 404

@pen_ody.route("/likes", methods=["POST"], strict_slashes=False)
@login_required
def create_like():
    """creates a new `Like` object"""
    user_id = request.json.get("user_id")
    blog_id = request.json.get("blog_id")
    if not user_id or not blog_id:
        return jsonify({"error": "blog_id and user_id is required"})
    like = Like()
    like.user_id = user_id
    like.blog_id = blog_id
    like.save()
    return jsonify({"success": like.id}), 201

@pen_ody.route("/likes/<string:like_id>", methods=["DELETE"], strict_slashes=False)
@login_required
def delete_like(like_id):
    """deletes the Like with the given `like_id`"""
    like = storage_engine.get(model="Like", id=like_id)
    if like:
        like.delete()
        return jsonify({"success": "like deleted"})
    return jsonify({"error": "like not found"}), 404
