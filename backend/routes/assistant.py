from flask import Blueprint, request, jsonify
from backend.services.assistant_service import assistant_service

assistant_bp = Blueprint("assistant", __name__, url_prefix="/api/assistant")


@assistant_bp.route("/ask", methods=["POST"])
def ask_assistant():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    if not message:
        return jsonify({"success": False, "message": "Message is required."}), 400
    return jsonify({"success": True, "answer": assistant_service.answer(message)})
