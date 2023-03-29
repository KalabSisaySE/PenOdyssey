#!/usr/bin/env python3

from api.v1.views import pen_ody
from flask import jsonify
from flask_login import LoginManager, login_required
from models.category import Category
from models import storage_engine

login_manager = LoginManager()
login_manager.init_app(pen_ody)


@pen_ody.route("/category/<string:cat_id>")
@login_required
def get_category(cat_id):
    """returns the category data"""
    cat_obj = storage_engine.get(model=Category, id=cat_id)
    return jsonify(cat_obj.to_json())