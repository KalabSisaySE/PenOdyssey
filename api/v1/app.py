#!/usr/bin/env python3
import bcrypt
import os
from flask import Flask, request ,jsonify, make_response, redirect, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import storage_engine
from api.v1.views import pen_ody

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint(pen_ody)

@login_manager.user_loader
def load_user(user_id):
    return storage_engine.get(model="User", id=user_id)

@app.route("/status")
def status():
    """status of the API"""
    return jsonify({"status": "API RUNNING"})

@app.route("/api/v1/login", methods=["POST"])
def login():
    """logs in the user by checking credentials"""
    if not current_user.is_authenticated:
        email = request.json.get("email")
        password = request.json.get("password")
        if not email or not password:
            return make_response(jsonify({"error": "email and password is required"}), 400)
        
        all_users = storage_engine.all(model="User")
        user = None
        if all_users:
            user = list(filter(lambda u: u.email == email, all_users))[0]
        if user:
            pass_byte = password.encode("utf-8")
            hashed_pass = user.password.encode("utf-8")
            
            if bcrypt.checkpw(pass_byte, hashed_pass):
                user = storage_engine.get(model="User", id=user.id)
                login_user(user, remember=False)
                return make_response(jsonify({"success": user.id}))

            return jsonify({"error": "invalid username or password"}), 401
        return jsonify({"error": "user not found"}), 404
    return redirect("/")

@app.route("/api/v1/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"success": "logged out successfully."})

@app.route("/")
@login_required
def home():
    """home for a logged in `User`"""
    return jsonify({"API": "PEN ODYSSEY V.1"})

@app.route('/checkauth')
def check_auth():
    """checks is session exists or not"""
    if current_user.is_authenticated:
        return jsonify({"session": current_user.__str__()})
    else:
        return jsonify({"session": "empty"})


if __name__ == "__main__":
    app.run(debug=True)