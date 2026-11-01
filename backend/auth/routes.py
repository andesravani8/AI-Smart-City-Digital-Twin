from flask import Blueprint, jsonify, request, session
from backend.auth.service import auth_service


auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    user = auth_service.authenticate(data.get("email"), data.get("password"))

    if not user:
        return jsonify({
            "success": False,
            "message": "Invalid email or password."
        }), 401

    session.clear()
    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    session["user_email"] = user["email"]
    session["user_role"] = user["role"]

    return jsonify({
        "success": True,
        "message": "Login successful.",
        "user": user,
        "redirect": "/dashboard"
    })


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True, "redirect": "/login"})


@auth_bp.route("/me", methods=["GET"])
def me():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"success": False, "authenticated": False}), 401

    user = auth_service.get_user(user_id)
    if not user:
        session.clear()
        return jsonify({"success": False, "authenticated": False}), 401

    return jsonify({"success": True, "authenticated": True, "user": user})
