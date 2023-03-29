#!/usr/bin/env python3
"""views for accessing blogs"""
from flask_login import LoginManager, login_required
from flask import jsonify
from api.v1.views import pen_ody
from models.blog import Blog
from models import storage_engine
from api.v1.views.utilities import fetch_blog_data

login_manager = LoginManager()
login_manager.init_app(pen_ody)



@pen_ody.route("/blogs/<string:blog_id>", strict_slashes=False)
@login_required
def get_blog(blog_id):
    """returns the blog for the given `blog_id`"""
    blog = storage_engine.get(model="Blog", id=blog_id)
    if blog:
        blog_data = blog.to_json()
        blog_data.update(
            {
                "written_by": f"http://127.0.0.1:5000/api/v1/users/{blog.user_id}",
                "blogs_tags": fetch_blog_data(model="Tag", blog=blog),
                "categorized_under": fetch_blog_data(model="BlogCategory", blog=blog),
                "bookmarks": fetch_blog_data(model="Bookmark", blog=blog),
                "comments": fetch_blog_data(model="Comment", blog=blog),
                "likes": fetch_blog_data(model="Like", blog=blog),
            }
        )
        return jsonify(blog_data)        
    return jsonify({"error": "Blog not found"})

@pen_ody.route("/blogs", strict_slashes=False)
@login_required
def get_all_blogs():
    """returns all the blogs data from the database"""
    all_blogs = storage_engine.all(model="Blog")
    if len(all_blogs) > 0:
        blogs = []
        for blog in all_blogs:
            blog_data = blog.to_json()
            blog_data.update(
                {
                    "written_by": f"http://127.0.0.1:5000/api/v1/users/{blog.user_id}",
                    "blogs_tags": fetch_blog_data(model="Tag", blog=blog),
                    "categorized_under": fetch_blog_data(model="BlogCategory", blog=blog),
                    "bookmarks": fetch_blog_data(model="Bookmark", blog=blog),
                    "comments": fetch_blog_data(model="Comment", blog=blog),
                    "likes": fetch_blog_data(model="Like", blog=blog),
                }
            )
            blogs.append(blog)
        return jsonify(blogs)

    return jsonify([])
