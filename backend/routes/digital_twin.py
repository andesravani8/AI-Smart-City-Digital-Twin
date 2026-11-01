# Flask route
from flask import Blueprint, request, jsonify

from backend.services.digital_twin_service import digital_twin_service


digital_twin_bp = Blueprint(
    "digital_twin",
    __name__,
    url_prefix="/api/digital-twin"
)


@digital_twin_bp.route("/", methods=["GET"])
def get_digital_twin():

    return jsonify({
        "success": True,
        "data": digital_twin_service.get_city()
    })


@digital_twin_bp.route("/zones", methods=["GET"])
def get_zones():

    return jsonify({
        "success": True,
        "zones": digital_twin_service.get_zones()
    })


@digital_twin_bp.route("/zones/<zone_id>", methods=["GET"])
def get_zone(zone_id):

    zone = digital_twin_service.get_zone(zone_id)

    if zone is None:

        return jsonify({
            "success": False,
            "message": "Zone not found."
        }), 404

    return jsonify({
        "success": True,
        "zone": zone
    })


@digital_twin_bp.route("/infrastructure", methods=["GET"])
def get_infrastructure():

    return jsonify({
        "success": True,
        "infrastructure":
            digital_twin_service.get_infrastructure()
    })


@digital_twin_bp.route("/zones/<zone_id>/status", methods=["PUT"])
def update_zone_status(zone_id):

    data = request.get_json()

    if not data or "status" not in data:

        return jsonify({
            "success": False,
            "message": "Status is required."
        }), 400

    zone = digital_twin_service.update_zone_status(
        zone_id,
        data["status"]
    )

    if zone is None:

        return jsonify({
            "success": False,
            "message": "Zone not found."
        }), 404

    return jsonify({
        "success": True,
        "zone": zone
    })