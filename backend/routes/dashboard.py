from flask import Blueprint, jsonify
from backend.database import database


dashboard_bp = Blueprint("dashboard", __name__)


# ==================================================
# DASHBOARD SUMMARY
# ==================================================

@dashboard_bp.route("/summary", methods=["GET"])
def dashboard_summary():

    connection = None
    cursor = None

    try:

        connection = database.get_connection()

        if connection is None:
            return jsonify({
                "success": False,
                "message": "Database connection failed"
            }), 500

        cursor = connection.cursor(dictionary=True)


        # --------------------------------------------------
        # 1. TOTAL CITY ZONES
        # --------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total_zones
            FROM city_zones
        """)

        total_zones = cursor.fetchone()["total_zones"]


        # --------------------------------------------------
        # 2. TOTAL INFRASTRUCTURE
        # --------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total_infrastructure
            FROM infrastructure
        """)

        total_infrastructure = cursor.fetchone()["total_infrastructure"]


        # --------------------------------------------------
        # 3. ACTIVE ALERTS
        # --------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS active_alerts
            FROM alerts
            WHERE status = 'active'
        """)

        active_alerts = cursor.fetchone()["active_alerts"]


        # --------------------------------------------------
        # 4. TOTAL PREDICTIONS
        # --------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total_predictions
            FROM predictions
        """)

        total_predictions = cursor.fetchone()["total_predictions"]


        # --------------------------------------------------
        # 5. LATEST PREDICTIONS
        # --------------------------------------------------

        cursor.execute("""
            SELECT
                id,
                module,
                prediction_value,
                risk_level,
                model_name,
                prediction_time
            FROM predictions
            ORDER BY prediction_time DESC
            LIMIT 20
        """)

        predictions = cursor.fetchall()


        # --------------------------------------------------
        # 6. CITY ZONE STATUS
        # --------------------------------------------------

        cursor.execute("""
            SELECT
                status,
                COUNT(*) AS count
            FROM city_zones
            GROUP BY status
        """)

        zone_status = cursor.fetchall()


        # --------------------------------------------------
        # 7. RECENT ALERTS
        # --------------------------------------------------

        cursor.execute("""
            SELECT
                id,
                module,
                title,
                message,
                severity,
                value,
                threshold,
                status,
                created_at
            FROM alerts
            ORDER BY created_at DESC
            LIMIT 10
        """)

        recent_alerts = cursor.fetchall()


        # --------------------------------------------------
        # FINAL RESPONSE
        # --------------------------------------------------

        return jsonify({

            "success": True,

            "summary": {

                "total_zones": total_zones,

                "total_infrastructure":
                    total_infrastructure,

                "active_alerts":
                    active_alerts,

                "total_predictions":
                    total_predictions
            },

            "predictions": predictions,

            "zone_status": zone_status,

            "recent_alerts": recent_alerts

        })


    except Exception as e:

        print("Dashboard API Error:", e)

        return jsonify({

            "success": False,

            "message":
                "Unable to load dashboard data",

            "error": str(e)

        }), 500


    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()