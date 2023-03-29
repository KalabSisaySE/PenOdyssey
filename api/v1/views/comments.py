#!/usr/bin/env python3
"""the `comments` module
contains the rotues to the model `Comment`"""

from flask_login import LoginManager, login_required
from flask import jsonify, request
from api.v1.views import pen_ody
from models import storage_engine
from models.comment import Comment


login_manager = LoginManager()
login_manager.init_app(pen_ody)

@pen_ody.route("/comments/<string:comm_id>", strict_slashes=False)
@login_required
def get_comment(comm_id):
    """returns the comments data"""
    comment = storage_engine.get(model="Comment", id=comm_id)
    if comment:
        return jsonify(comment.to_json())
    return jsonify({"error": "comment not found"}), 404


@pen_ody.route("/comments", methods=["POST"], strict_slashes=False)
@login_required
def create_comment():
    """creates a new `Comment` object"""
    user_id = request.json.get("user_id")
    blog_id = request.json.get("blog_id")
    user_comment = request.json.get("user_comment")
    if not user_id or not blog_id or not user_comment:
        return jsonify({"error": "blog_id, user_id and user_comment are required"})
    comm = Comment()
    comm.user_id = user_id
    comm.blog_id = blog_id
    comm.user_comment = user_comment
    comm.save()
    return jsonify({"success": comm.id}), 201

@pen_ody.route("/comments/<string:comm_id>", methods=["PUT"], strict_slashes=False)
@login_required
def update_comment(comm_id):
    """creates a new `Comment` object"""
    user_comment = request.json.get("user_comment")
    if not user_comment:
        return jsonify({"error": "user_comment is required"})
    comm = storage_engine.get(model=Comment, id=comm_id)
    comm.user_comment = user_comment
    comm.save()
    return jsonify({"success": "comment changed successfully"})

@pen_ody.route("/comments/<string:comm_id>", methods=["DELETE"], strict_slashes=False)
@login_required
def delete_comment(comm_id):
    """deletes the comment with the given `comm_id`"""
    comment = storage_engine.get(model="Comment", id=comm_id)
    if comment:
        comment.delete()
        return jsonify({"success": "comment deleted"})
    return jsonify({"error": "comment not found"}), 404
