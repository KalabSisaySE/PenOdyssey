#!/usr/bin/env python3
"""the `users` modules
routes for the user model
"""
from flask import jsonify, make_response, request
from flask_login import LoginManager, login_required, current_user
from typing import List, TypeVar
from api.v1.views import pen_ody
from api.v1.views.utilities import fetch_user_data
from models.user import User
from models import storage_engine

log_manager = LoginManager()
log_manager.init_app(pen_ody)


def check_user_attrs(data: dict) -> str:
    """checks if all the required attributes exists in the request"""


@pen_ody.route("/users/<string:user_id>", strict_slashes=False)
@login_required
def get_user(user_id):
    """get the user with the given id"""
    if user_id == "me":
       user = current_user
    else:
       user = storage_engine.get(model="User", id=user_id)
    if user:
        user_data = user.to_json()
        user_data.pop("email", None)
        user_data.update(
            {
                "written_blogs": fetch_user_data(model="Blog", user=user),
                "bookmarked_blogs": fetch_user_data(model="Bookmark", user=user),
                "comments": fetch_user_data(model="Comment", user=user),
                "likes": fetch_user_data(model="Like", user=user),
                "subscribed_to": fetch_user_data(model="Subscription", user=user)[0].get("subscriber_id", []),
                "subscribers": fetch_user_data(model="Subscription", user=user)[1].get("writer_id", [])
            }
        )
        return jsonify(user_data)

    return make_response(jsonify({"error": "user is not found"}))

@pen_ody.route("/users", strict_slashes=False)
@login_required
def get_all_users():
    """returns a list of all users from the database"""
    all_users = storage_engine.all(model=User)
    if len(all_users) > 0:
        users = []
        for user in all_users:
            user_data = user.to_json()
            user_data.pop("email", None)
            user_data.update(
                {
                    "written_blogs": fetch_user_data(model="Blog", user=user),
                    "bookmarked_blogs": fetch_user_data(model="Bookmark", user=user),
                    "comments": fetch_user_data(model="Comment", user=user),
                    "likes": fetch_user_data(model="Like", user=user),
                    "subscribed_to": fetch_user_data(model="Subscription", user=user)[0]["subscriber_id"],
                    "subscribers": fetch_user_data(model="Subscription", user=user)[1]["writer_id"]
                }
            )
            users.append(user_data)
        return jsonify(user_data)
    return jsonify([])

@pen_ody.route("/users", methods=["POST"], strict_slashes=False)
@login_required
def create_user():
    """creates a new user"""
    emails = [user.email for user in storage_engine.all(model=User)]
    req_attrs = {
        "email": request.json.get("email"),
        "password": request.json.get("password"),
        "first_name": request.json.get("first_name"),
        "last_name": request.json.get("last_name"),
        "bio": request.json.get("bio"),
        "interests": request.json.get("interests")
    }
    for attr in req_attrs:
        if not req_attrs[attr]:
            return jsonify({"error": f"missing {attr}"})
    if req_attrs["email"] in emails:
        return jsonify({"error": "email already exists, use a different email"})
    user = User()
    for key, val in req_attrs.items():
        setattr(user, key, val)
    user.save()
    return jsonify({"success": user.id}), 201

@pen_ody.route("/users/me", methods=["PUT"], strict_slashes=False)
@login_required
def edit_user():
    """edits the loggedin user"""
    user = current_user
    attrs = ["email", "password", "first_name", "last_name", "bio", "interests"]
    if request.json:
        for key, val in request.json.items():
            if key in attrs:
                setattr(user, key, val)
        user.save()
        return jsonify({"success": "changed successfully"})
    return jsonify({"error": "failed to update user"})

@pen_ody.route("/users/<string:user_id>", methods=["DELETE"], strict_slashes=False)
@login_required
def delete_user(user_id):
    """deletes the user with the given `user_id`"""
    user = storage_engine.get(model=User, id=user_id)
    if user:
        return jsonify({"success": "user deleted successfully"})
    return jsonify({"error": "user is not found"}), 404
