# Flask route
from flask import Blueprint, request, jsonify

from backend.services.alert_service import alert_service


alerts_bp = Blueprint(
    "alerts",
    __name__,
    url_prefix="/api/alerts"
)


@alerts_bp.route("/", methods=["GET"])
def get_alerts():

    return jsonify({
        "success": True,
        "alerts": alert_service.get_alerts()
    })


@alerts_bp.route("/active", methods=["GET"])
def get_active_alerts():

    return jsonify({
        "success": True,
        "alerts": alert_service.get_active_alerts()
    })


@alerts_bp.route("/create", methods=["POST"])
def create_alert():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Alert data is required."
        }), 400

    required_fields = [
        "module",
        "level",
        "title",
        "message"
    ]

    for field in required_fields:

        if field not in data:

            return jsonify({
                "success": False,
                "message": f"{field} is required."
            }), 400

    alert = alert_service.create_alert(
        module=data["module"],
        level=data["level"],
        title=data["title"],
        message=data["message"],
        value=data.get("value"),
        threshold=data.get("threshold")
    )

    return jsonify({
        "success": True,
        "alert": alert
    })


@alerts_bp.route("/resolve/<int:alert_id>", methods=["PUT"])
def resolve_alert(alert_id):

    result = alert_service.clear_alert(alert_id)

    if not result:

        return jsonify({
            "success": False,
            "message": "Alert not found."
        }), 404

    return jsonify({
        "success": True,
        "message": "Alert resolved successfully."
    })