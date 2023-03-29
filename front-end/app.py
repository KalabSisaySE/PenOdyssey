#!/usr/bin/env python3
"""the app module
contains the flasks application
"""
from flask import Flask, render_template, request, url_for, session, redirect, abort
import os
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")


@app.route("/login", methods=["POST", "GET"], strict_slashes=False)
def login():
    """renders the login page"""    
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if not email or not password:
            return "Email and Password is required"
        else:
            login_url = "http://127.0.0.1:5000/api/v1/login"
            user_data = {
                "email": email, 
                "password": password
            }
            login_response = requests.post(login_url, json=user_data)
            if login_response.status_code == 200:
                session["u_cookie"] = login_response.cookies.get("session")
                user_url = "http://127.0.0.1:5000/api/v1/users/me"
                user_res = requests.get(user_url, cookies={"session": session.get("u_cookie")})
                data = user_res.json()
                session["user_data"] = data
                return redirect(url_for("user_profile"))
            elif "error" in login_response.json():
                abort(404)

@app.route("/blog/<string:blog_id>", strict_slashes=False)
def blog(blog_id):
    """renders the login page"""
    if session.get("u_cookie"):
        sess_cookie = {"session": session.get("u_cookie")} 
        url = "http://127.0.0.1:5000/api/v1/blogs/" + blog_id
        # s = requests.Session()
        blog_res = requests.get(url, cookies=sess_cookie)
        if blog_res.status_code == 200:
            # FOR TAGS
            if len(blog_res.json().get("blogs_tags")):
                tag_links = blog_res.json().get("blogs_tags")
                tags = [requests.get(tag_link, cookies=sess_cookie).json().get("tag_name") for tag_link in tag_links]
            else:
                tags = None

            # FOR CATEGORIES
            if len(blog_res.json().get("categorized_under")) > 0:
                blog_cates = blog_res.json().get("categorized_under")
                cate_links = [f'http://127.0.0.1:5000/api/v1/category/{requests.get(link, cookies=sess_cookie).json().get("category_id")}' for link in blog_cates]
                cat_names = [requests.get(cat_link, cookies=sess_cookie).json().get("category_name") for cat_link in cate_links ]
                blog_copy = blog_res.json().copy()
                blog_copy["blog_content"] = blog_copy["blog_content"].split("\n")
            else:
                cat_names = None
                blog_copy = None

            # FOR LIKES - format ["user_name"]
            if len(blog_res.json().get("likes")) > 0:
                likes_links = blog_res.json().get("likes")
                user_links = [requests.get(like_link, cookies=sess_cookie).json().get("user_id") for like_link in likes_links ]
                user_who_liked = [get_users_fullname(user_link) for user_link in user_links]
            else:
                user_who_liked = None

            # FOR COMMENTS - format {"comment": ["user_full_name", "user_id"]}
            if len(blog_res.json().get("comments")) > 0:
                comments = blog_res.json().get("comments")
                comment_user = {
                    requests.get(comment, cookies=sess_cookie).json().get("user_comment"): [
                        get_users_fullname(requests.get(comment, cookies=sess_cookie).json().get("user_id")),
                        requests.get(comment, cookies=sess_cookie).json().get("user_id")
                    ] 
                    for comment in comments}
            else:
                comment_user = None

            return render_template("blog.html", blog=blog_copy, tags=tags, categories=cat_names, likes=user_who_liked, comments=comment_user)
    return "Unauthorized"
                    
@app.route("/user_profile", strict_slashes=False)
def user_profile():
    """main view function for a user's profile"""
    if session.get("u_cookie"):
        sess_cookie = {"session": session.get("u_cookie")} 
        url = "http://127.0.0.1:5000/api/v1/users/me"
        res = requests.get(url, cookies=sess_cookie)
        if res.status_code == 200:

            # My Blogs Section
            if len(res.json().get("written_blogs")) > 0:
                blog_urls = res.json().get("written_blogs")
                written_blogs = {requests.get(blog_url, cookies=sess_cookie).json().get("blog_title"): blog_url[blog_url.rfind("/"):]
                    for blog_url in blog_urls
                }
            else:
                written_blogs=None

            # Bookmarks Section
            if len(res.json().get("bookmarked_blogs")) > 0:
                blog_urls = res.json().get("bookmarked_blogs")
                bookmarked_blogs = {requests.get(blog_url, cookies=sess_cookie).json().get("blog_title"): blog_url[blog_url.rfind("/"):]
                    for blog_url in blog_urls
                }
            else:
                bookmarked_blogs=None

            # Liked Blogs section
            if len(res.json().get("likes")) > 0:
                like_urls = res.json().get("likes")
                blog_urls = [f"http://127.0.0.1:5000/api/v1/blogs/{requests.get(like_url, cookies=sess_cookie).json().get('blog_id')}"
                    for like_url in like_urls
                ]
                liked_blogs = {requests.get(blog_url, cookies=sess_cookie).json().get("blog_title"): blog_url[blog_url.rfind("/"):]
                    for blog_url in blog_urls
                }
            else:
                liked_blogs=None

            # comments
            if len(res.json().get("comments")) > 0:
                comms = res.json().get("comments")
                comment_texts = [requests.get(comm, cookies=sess_cookie).json().get("user_comment") for comm in comms]

            # Subscribed to
            if len(res.json().get("subscribed_to")) > 0:
                subscriptions = res.json().get("subscribed_to")
                user_links = [f'http://127.0.0.1:5000/api/v1/users/{requests.get(sub, cookies=sess_cookie).json().get("writer_id")}' for sub in subscriptions]
                subscribed_to = {} 
                for user_link in user_links:
                    user = requests.get(user_link, cookies=sess_cookie).json()
                    subscribed_to.update({f"{user.get('first_name')} {user.get('last_name')}": user_link[user_link.rfind('/'):]})
            else:
                subscribed_to = None

            # Subscribers
            if len(res.json().get("subscribers")) > 0:
                subscriptions = res.json().get("subscribers")
                user_links = [f'http://127.0.0.1:5000/api/v1/users/{requests.get(sub, cookies=sess_cookie).json().get("subscriber_id")}' for sub in subscriptions]
                subscribers = {}
                for user_link in user_links:
                    user = requests.get(user_link, cookies=sess_cookie).json()
                    subscribers.update({f"{user.get('first_name')} {user.get('last_name')}": user_link[user_link.rfind('/'):]})
            else:
                subscribers = None

            return render_template(
                "user_profile.html",
                user=session.get("user_data"),
                written_blogs=written_blogs,
                bookmarked_blogs=bookmarked_blogs,
                liked_blogs=liked_blogs,
                comments=comment_texts,
                subscribed_to=subscribed_to,
                subscribers=subscribers
            )
        else:
            return render_template(
                "user_profile.html",
                user=session.get("user_data")
            )
        
@app.route("/user/<string:user_id>", strict_slashes=False)
def user(user_id):
    """view function for a user data"""
    if session.get("u_cookie"):
        sess_cookie = {"session": session.get("u_cookie")} 
        url = "http://127.0.0.1:5000/api/v1/users/" + user_id
        res = requests.get(url, cookies=sess_cookie)
        if res.status_code == 200:

            # My Blogs Section
            if len(res.json().get("written_blogs")) > 0:
                blog_urls = res.json().get("written_blogs")
                written_blogs = {requests.get(blog_url, cookies=sess_cookie).json().get("blog_title"): blog_url[blog_url.rfind("/"):]
                    for blog_url in blog_urls
                }
            else:
                written_blogs=None

            # Bookmarks Section
            if len(res.json().get("bookmarked_blogs")) > 0:
                blog_urls = res.json().get("bookmarked_blogs")
                bookmarked_blogs = {requests.get(blog_url, cookies=sess_cookie).json().get("blog_title"): blog_url[blog_url.rfind("/"):]
                    for blog_url in blog_urls
                }
            else:
                bookmarked_blogs=None

            # Liked Blogs section
            if len(res.json().get("likes")) > 0:
                like_urls = res.json().get("likes")
                blog_urls = [f"http://127.0.0.1:5000/api/v1/blogs/{requests.get(like_url, cookies=sess_cookie).json().get('blog_id')}"
                    for like_url in like_urls
                ]
                liked_blogs = {requests.get(blog_url, cookies=sess_cookie).json().get("blog_title"): blog_url[blog_url.rfind("/"):]
                    for blog_url in blog_urls
                }
            else:
                liked_blogs=None

            # comments
            if len(res.json().get("comments")) > 0:
                comms = res.json().get("comments")
                comment_texts = [requests.get(comm, cookies=sess_cookie).json().get("user_comment") for comm in comms]

            # Subscribed to
            if len(res.json().get("subscribed_to")) > 0:
                subscriptions = res.json().get("subscribed_to")
                user_links = [f'http://127.0.0.1:5000/api/v1/users/{requests.get(sub, cookies=sess_cookie).json().get("writer_id")}' for sub in subscriptions]
                subscribed_to = {} 
                for user_link in user_links:
                    user = requests.get(user_link, cookies=sess_cookie).json()
                    subscribed_to.update({f"{user.get('first_name')} {user.get('last_name')}": user_link[user_link.rfind('/'):]})
            else:
                subscribed_to = None

            # Subscribers
            if len(res.json().get("subscribers")) > 0:
                subscriptions = res.json().get("subscribers")
                user_links = [f'http://127.0.0.1:5000/api/v1/users/{requests.get(sub, cookies=sess_cookie).json().get("subscriber_id")}' for sub in subscriptions]
                subscribers = {}
                for user_link in user_links:
                    user = requests.get(user_link, cookies=sess_cookie).json()
                    subscribers.update({f"{user.get('first_name')} {user.get('last_name')}": user_link[user_link.rfind('/'):]})
            else:
                subscribers = None

            return render_template(
                "user_profile.html",
                user=res.json(),
                written_blogs=written_blogs,
                bookmarked_blogs=bookmarked_blogs,
                liked_blogs=liked_blogs,
                comments=comment_texts,
                subscribed_to=subscribed_to,
                subscribers=subscribers
            )
        else:
            return render_template(
                "user_profile.html",
                user=res.json()
            )

def get_users_fullname(link: str) -> str:
    """fetches user data using `link` or `id` and `cookie`"""
    if session.get("u_cookie"):
        sess_cookie = {"session": session.get("u_cookie")}
        if not link.startswith("http"):
            u_link = "http://127.0.0.1:5000/api/v1/users/" + link
        else:
            u_link = link
        return requests.get(u_link, cookies=sess_cookie).json().get("first_name") + " " + requests.get(u_link, cookies=sess_cookie).json().get("last_name")
    else:
        "SESSION NOT SET"

if __name__ == "__main__":
    app.run(
        port=6555,
        debug=True,
    )