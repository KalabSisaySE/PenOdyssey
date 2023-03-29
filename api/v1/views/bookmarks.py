#!/usr/bin/env python3
"""the `bookmarks module`
contains the rotues to the model `Bookmark`"""

from flask_login import LoginManager, login_required
from flask import jsonify, request
from api.v1.views import pen_ody
from models import storage_engine
from models.bookmark import Bookmark

login_manager = LoginManager()
login_manager.init_app(pen_ody)

@pen_ody.route("/bookmarks/<string:bk_id>")
@login_required
def get_bookmark(bk_id):
    """returns the bookmarks data"""
    bookmark = storage_engine.get(model="Bookmark", id=bk_id)
    if bookmark:
        return jsonify(bookmark.to_json())
    return jsonify({"error": "bookmark not found"}), 404

@pen_ody.route("/bookmarks", methods=["POST"], strict_slashes=False)
@login_required
def create_bookmark():
    """creates a new `Bookmark` object"""
    user_id = request.json.get("user_id")
    blog_id = request.json.get("blog_id")
    if not user_id or not blog_id:
        return jsonify({"error": "blog_id and user_id are required"})
    bk = Bookmark()
    bk.user_id = user_id
    bk.blog_id = blog_id
    bk.save()
    return jsonify({"success": bk.id}), 201

@pen_ody.route("/bookmarks/<string:bk_id>")
@login_required
def delete_bookmark(bk_id):
    """deletes the bookmark with the given `bk_id`"""
    bookmark = storage_engine.get(model="Bookmark", id=bk_id)
    if bookmark:
        bookmark.delete()
        return jsonify({"success": "bookmark deleted"})
    return jsonify({"error": "bookmark not found"}), 404
