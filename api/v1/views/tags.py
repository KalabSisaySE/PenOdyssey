#!/usr/bin/env python3
"""the `tags` module
contains the rotues to the model `Tag`"""

from flask_login import LoginManager, login_required
from flask import request, jsonify
from api.v1.views import pen_ody
from models import storage_engine
from models.tag import Tag

login_manager = LoginManager()
login_manager.init_app(pen_ody)

@pen_ody.route("/tags/<string:tag_id>")
@login_required
def get_tag(tag_id):
    """returns the tags data"""
    tag = storage_engine.get(model="Tag", id=tag_id)
    if tag:
        return jsonify(tag.to_json())
    return jsonify({"error": "tag not found"}), 404

@pen_ody.route("/tags", methods=["POST"], strict_slashes=False)
@login_required
def create_tag():
    """creates a new `Tag` object"""
    tag_name = request.json.get("tag_name")
    blog_id = request.json.get("blog_id")
    if not tag_name or not blog_id:
        return jsonify({"error": "blog_id and tag_name are required"})
    tag = Tag()
    tag.tag_name = tag_name
    tag.blog_id = blog_id
    tag.save()
    return jsonify({"success": tag.id}), 201

@pen_ody.route("/bookmarks/<string:tag_id>", methods=["DELETE"], strict_slashes=False)
@login_required
def delete_tag(tag_id):
    """deletes the bookmark with the given `bk_id`"""
    tag = storage_engine.get(model="Bookmark", id=tag_id)
    if tag:
        tag.delete()
        return jsonify({"success": "tag deleted"})
    return jsonify({"error": "tag not found"}), 404

