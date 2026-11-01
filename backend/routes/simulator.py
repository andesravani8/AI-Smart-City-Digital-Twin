# Flask route
from flask import Blueprint, request, jsonify

from backend.services.simulation_service import simulation_service


simulator_bp = Blueprint(
    "simulator",
    __name__,
    url_prefix="/api/simulator"
)


@simulator_bp.route("/run", methods=["POST"])
def run_simulation():

    data = request.get_json()

    if not data:

        return jsonify({
            "success": False,
            "message": "Simulation input is required."
        }), 400

    try:

        result = simulation_service.run_simulation(data)

        return jsonify({
            "success": True,
            "simulation": result
        })

    except ValueError:

        return jsonify({
            "success": False,
            "message": "Simulation values must be numbers."
        }), 400

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@simulator_bp.route("/history", methods=["GET"])
def simulation_history():

    return jsonify({
        "success": True,
        "history": simulation_service.get_history()
    })