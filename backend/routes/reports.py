from flask import Blueprint, jsonify
from backend.services.report_service import report_service

reports_bp = Blueprint("reports", __name__, url_prefix="/api/reports")


@reports_bp.route("/summary", methods=["GET"])
def report_summary():
    return jsonify({"success": True, "report": report_service.summary()})
