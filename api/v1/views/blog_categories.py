#!/usr/bin/env python3

from api.v1.views import pen_ody
from flask import jsonify
from flask_login import LoginManager, login_required
from models.blog_category import BlogCategory
from models import storage_engine

login_manager = LoginManager()
login_manager.init_app(pen_ody)


@pen_ody.route("/blogcategory/<string:bc_id>")
@login_required
def get_blog_category(bc_id):
    """returns the category data"""
    obj = storage_engine.get(model=BlogCategory, id=bc_id)
    return jsonify(obj.to_json())