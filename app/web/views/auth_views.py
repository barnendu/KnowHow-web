from flask import Blueprint, g, request, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from app.web.db.models import User

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route("/user", methods=["GET"])
def get_user():
    if g.user is not None:
        return g.user.as_dict()
    
    return jsonify(None)

@bp.route("/signin", methods=["POST"])
def signin():
    data = request.get_json()
    user = User.find_by(email=data["email"])
    if user is None:
        return jsonify(None)
    if not check_password_hash(user.password, data["password"]):
        return { "message": "Invalid password" }, 400
    session.permanent =True
    session["user_id"] = user.id
    return user.as_dict()

@bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    user = User.create(email=data["email"], password=generate_password_hash(data["password"]))
    session.permanent = True
    session["user_id"] = user.id
    return user.as_dict()

@bp.route("/signout", methods=["POST"])
def signout():
    session.clear()
    return {"message": "Signed out successfully"}